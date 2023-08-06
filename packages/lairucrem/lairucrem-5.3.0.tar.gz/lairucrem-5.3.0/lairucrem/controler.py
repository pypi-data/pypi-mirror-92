#! /usr/bin/env python
# Copyright (C) 2016 Alain Leufroy
#
# Author: Alain Leufroy <alain@leufroy.fr>
# Licence: WTFPL, grab your copy here: http://sam.zoy.org/wtfpl/
"""Controller that manage data and connect widgets."""
import asyncio
import re
from collections import defaultdict
from functools import partial
from pathlib import Path

import urwid

from . import config, mixin, open_popup, process, widgets
from .mixin import ensurable, multilist, paginatedlist, waitable
from .utils import (ParseError, ensure_one, nodestr, parse_colored_line,
                    popup_error, shelvestr)
from .widgets import attrwrap, dialog, mainwidget


class _multiwalker(
        ensurable, waitable, multilist, urwid.SimpleFocusListWalker):
    """Waitable multiwalker.

    All sub walkers are ensured/delayed/cancelled all together.

    Signals:

    - 'completed': fired when the output of the hg sub command as been fully
                   loaded.
    """

    signals = ['completed']

    def __init__(self, walkers):
        self.__sequences__ = walkers
        for walker in walkers:
            urwid.signals.connect_signal(walker, 'modified', self._modified)
        super().__init__([])

    async def _wait(self):
        await super()._wait()
        await asyncio.gather(*(walker.wait() for walker in self.__sequences__))
        urwid.emit_signal(self, 'completed')

    async def stop(self):
        await asyncio.gather(*(walker.stop() for walker in self.__sequences__))


class _hgwalker(ensurable, waitable, urwid.SimpleFocusListWalker):
    """An waitable walker though stdout of an async hg process.

    Signals:

    - 'completed': fired when the output of the hg sub command as been fully
                   loaded.
    """

    cmd = ('--verbose', 'help')

    signals = ['completed']

    class line_widget(mixin.focusable_widget, urwid.Text):
        pass

    def __init__(self, *args, **kwargs):
        self.hgproc = None
        super().__init__([urwid.Text('LOADING …')], *args, **kwargs)

    def get_cmd(self):
        return self.cmd

    async def __aiter__(self):
        async for line in self.aiterlines():
            widget = self._get_widget(line)
            if widget:
                yield widget

    async def aiterlines(self):
        cmd = self.get_cmd()
        if not cmd:
            return
        if self.hgproc:
            await self.hgproc.kill()
        self.hgproc = process.hg(*cmd)
        await self.hgproc.start()
        try:
            async for line in self.hgproc:
                yield line
        except asyncio.CancelledError:
            # raised when the task is interrupted
            await self.hgproc.kill()

    def _get_widget(self, line):
        content = self._parse_line(line)
        if not content:
            return None
        return self._make_widget(content)

    def _parse_line(self, line):
        return parse_colored_line(line.rstrip())

    def _make_widget(self, content):
        return self.line_widget(content)

    async def _wait(self):
        await super()._wait()
        first = True
        async with config.PROCESSES_SEMAPHORE:
            async for widget in self:
                if first:
                    self.clear(full=True)
                    first = False
                self.append(widget)
        if first:               # nothing fetched
            self.clear(full=True)
        urwid.emit_signal(self, 'completed')

    def clear(self, full=False):
        super().clear()
        if not full:
            self.append(urwid.Text('LOADING …'))

    async def stop(self):
        if self.hgproc:
            await self.hgproc.kill()
        super().cancel()


class _listbox(ensurable, waitable, mixin.mouse_up_down, urwid.ListBox):
    """An waitable listbox that handle waitable walkers."""

    def __init__(self, walker, *walkers, **kwargs):
        if walkers:
            walker = _multiwalker((walker,) + walkers)
        super().__init__(walker, **kwargs)
        self._connect_all()

    def _connect_all(self):
        urwid.signals.connect_signal(
            self.body, 'modified', self._on_modified)

    def _on_modified(self, *args):
        # reset the view when the first line arrived
        return

    async def _wait(self):
        if self.body:
            self.body.set_focus(0)
            self.set_focus(0)
        else:
            self.set_focus_pending = None
            self.set_focus_valign_pending = None
        await self.body._wait()

    def _set_focus_complete(self, size, focus):
        if self.body:
            super()._set_focus_complete(size, focus)

    def _set_focus_valign_complete(self, size, focus):
        if self.body:
            super()._set_focus_valign_complete(size, focus)

    def cancel(self):
        self.body.cancel()

    async def stop(self):
        await self.body.stop()

    def set_focus(self, position, coming_from=None):
        try:
            return super().set_focus(position, coming_from)
        except IndexError:
            # The list is empty, just ignore it
            pass


class _graphtree:

    class line_widget(
            mixin.focusable_widget,
            mixin.horizontal_scroll_text,
            mixin.highlightable_widget,
            mixin.selectable_widget,
            mixin.one_line_widget,
            urwid.Text):
        pass


class cwdwalker(_graphtree, _hgwalker):

    cmd = ('diff', '--stat')

    async def __aiter__(self):
        has_no_changes = True
        async for widget in super().__aiter__():
            if widget:
                has_no_changes = False
                yield widget
        if has_no_changes:
            yield self._make_widget([('', '')])

    def _parse_line(self, line):
        line = super()._parse_line(line)
        return line if len(line) == 1 else None

    def _make_widget(self, content):
        content = [('', '@  CWD ')] + content
        widget = super()._make_widget(content)
        widget.node = None
        widget.p1 = -1
        return widget


class shelvewalker(_graphtree, _hgwalker):

    cmd = ('--config', 'extensions.shelve=', 'shelve', '--list')

    def _make_widget(self, content):
        name = content[0][-1]
        content = [('', '|  ')] + [
            (style or 'shelve.description', txt) for style, txt in content]
        widget = super()._make_widget(content)
        widget.node = shelvestr(name)
        return widget


class changesetwalker(
        _graphtree,
        mixin.modifiable_widget,
        paginatedlist,
        _hgwalker):

    _sep = '\0\0'
    _template = r'\0\0' + r'\0\0'.join([
        '{node}', '{rev}', '{graphnode}', '{p1rev}', '{children}', config.TEMPLATE])

    class graph_line_widget(
            mixin.horizontal_scroll_text,
            mixin.one_line_widget,
            urwid.Text):
        pass

    class cwd_line_widget(
            attrwrap,
            _graphtree.line_widget):

        _attr_map = {None: 'log.cwd'}
        _focus_map = {None: 'log.cwd.focus'}

    def __init__(self, rev, hidden, *args, **kwargs):
        self.rev = rev
        self.hidden = hidden
        super().__init__(*args, **kwargs)

    def get_cmd(self):
        cmd = ['--config', 'ui.graphnodetemplate=%s' % config.GRAPHNODETEMPLATE,
               'debuglairucremgraphlog',
               '--template', self._template]
        if self.rev:
            cmd += ['--rev', self.rev]
        if self.hidden:
            cmd += ['--hidden']
        return cmd

    def _get_widget(self, line):
        line = line.rstrip()
        if line.count(self._sep) == 6:
            return self.make_commit_widget(line)
        else:
            return self.make_graph_widget(line)

    def make_commit_widget(self, line):
        data = line.split(self._sep)
        try:
            graph, node, rev, graphnode, p1, children, content = data
        except ValueError:
            raise ParseError(f'Unexpected output: {data}')
        if set(node) == {'f'}:
            return
        iscwd = graphnode == '@'
        content = self._parse_graph(graph) + self._parse_content(content)
        widget = self._make_widget(content)
        if iscwd:
            widget = self.cwd_line_widget(content)
        widget.node = nodestr(node)
        widget.rev = int(rev)
        widget.p1 = int(p1)
        widget.cwd = iscwd
        widget.children = [
            int(child.split(':')[0]) for child in children.split()]
        urwid.signals.connect_signal(widget, 'modified', self._modified)
        return widget

    def make_graph_widget(self, line):
        if not (set(line) - set(' |:')):
            # skip useless graph lines
            return
        return self.graph_line_widget(parse_colored_line(line))

    def _parse_content(self, content):
        return parse_colored_line(content)

    def _parse_graph(self, graph):
        return parse_colored_line(graph)

    async def find_widget(self, matcher):
        """Return (widget, position) of the cset with the given rev."""
        # search in already loaded csets
        async for widget, position in self.iter_widgets():
            if matcher(widget):
                return widget, position
        else:
            raise mixin.NotFound(f'Not Found')

    async def get_rev(self, rev):
        """Return (widget, position) of the cset with the given rev."""
        # search in already loaded csets
        return await self.find_widget(partial(self._is_widget_match_rev, rev))

    @staticmethod
    def _is_widget_match_rev(rev, widget):
        return ((rev == -1 and getattr(widget, 'cwd', None))
                or (getattr(widget, 'rev', None) == rev))

    async def _wait(self):
        async with popup_error(OSError, donotraise=True):
            await super()._wait()


class _patchdetailwalker(_hgwalker):

    class line_widget(
            mixin.highlightable_widget,
            mixin.focusable_widget,
            urwid.Text):
        pass

    def __init__(self, node=None, *args, **kwargs):
        self.node = node
        super().__init__(*args, **kwargs)


class diffstatwalker(_patchdetailwalker):
    """Manage diff content."""

    signals = ['link']
    filename = None

    class line_widget(
            mixin.link,
            mixin.selectable_widget,
            mixin.highlightable_widget,
            mixin.focusable_widget,
            urwid.Text):
        pass

    def get_cmd(self):
        if self.node is None:
            cmd = ['diff', '--stat']
        elif isinstance(self.node, nodestr):
            cmd = ['--hidden', 'diff', '--stat', '--change', self.node]
        elif isinstance(self.node, shelvestr):
            return ['shelve', '--stat', self.node]
        else:
            return None
        if self.filename:
            cmd += filter_files(self.filename)
        return cmd

    def _parse_line(self, line):
        if '|' not in line:     # skip the summary
            return
        return parse_colored_line(line.rstrip())

    def _make_widget(self, content):
        widget = super()._make_widget(content)
        widget.fname = fname = content[0][1].split('|')[0].strip()
        # propagate signal
        urwid.connect_signal(
            widget, 'link', lambda w, *args: urwid.emit_signal(self, 'link', fname, *args))
        return widget


class diffwalker(_patchdetailwalker):
    """Manage diff content."""

    filename = None

    class diff_line_widget(
            attrwrap,
            _patchdetailwalker.line_widget):

        _attr_map = {None: 'diff.diffline'}
        _focus_map = {None: 'diff.diffline.focus'}

    def get_cmd(self):
        if self.node is None:
            cmd = ['--verbose', 'diff']
        elif isinstance(self.node, nodestr):
            cmd = [
                '--verbose', '--hidden',
                'diff',
                '--git', '--nodates', '--noprefix',
                '--show-function', '--change', self.node
            ]
        elif isinstance(self.node, shelvestr):
            return ['--verbose', 'shelve', '--patch', self.node]
        else:
            return None
        if self.filename:
            cmd += filter_files(self.filename)
        return cmd

    def _parse_line(self, line):
        return parse_colored_line(line.rstrip(), default_style='diff.context')

    def _make_widget(self, content):
        widget = super()._make_widget(content)
        try:
            if content[0][0] == 'diff.diffline':
                widget = self.diff_line_widget(content)
        finally:
            return widget


class summarywalker(_patchdetailwalker):
    """Manage the cset summary content."""

    def get_cmd(self):
        if self.node is None:
            return ('--verbose', 'summary')
        elif isinstance(self.node, nodestr):
            return ('--verbose', '--hidden', 'log', '--hidden', '--template', config.SUMMARY_TEMPLATE,
                    '-r', self.node)
        else:
            return None


class summaryextrawalker(_patchdetailwalker):
    """Manage the cset summary extras content."""

    def get_cmd(self):
        if isinstance(self.node, nodestr):
            return ('--verbose', '--hidden', 'log', '--template', config.SUMMARY_EXTRA_TEMPLATE,
                    '-r', self.node)
        else:
            return None


class descriptionwalker(_patchdetailwalker):
    """Manage the cset description content."""

    def get_cmd(self):
        if isinstance(self.node, nodestr):
            return ('--hidden', 'log', '--template', r'\n{desc}\n\n', '--rev', self.node)
        else:
            return None

    def _make_widget(self, content):
        content = [(style or 'log.description', text)
                   for style, text in content]
        widget = super()._make_widget(content)
        return urwid.AttrWrap(
            widget, 'log.description', 'log.description.focus')


class graphlistbox(
        mixin.horizontal_scroll_listbox,
        mixin.changeable_listbox,
        mixin.filterable_listbox,
        mixin.searchable_listbox,
        mixin.commandable_listbox,
        mixin.refreshable_listbox,
        _listbox):
    """Manage the cset tree."""

    def __init__(self, rev, hidden, *args):
        self._cwd = cwdwalker()
        self._changeset = changesetwalker(rev, hidden)
        self._shelve = shelvewalker()  # shelvewalker()
        self.on_filter = ensure_one(self._on_filter)
        self.on_commandlist = ensure_one(self._on_commandlist)
        self.reset_commands_selectors = ensure_one(self._reset_commands_selectors)
        self.on_focus_rev = ensure_one(self._on_focus_rev)
        super().__init__(self._cwd, self._shelve, self._changeset)

    def _connect_all(self):
        super()._connect_all()
        urwid.connect_signal(self, 'filter', self.on_filter.ensure)
        urwid.signals.connect_signal(self, 'refresh', lambda *a: self.ensure())

    def connect_commands(self):
        # 1) Delay reset_commands_selector to prevent starting processes while
        # quickly browsing the history.
        # 2) IMPORTANT: 'on_commandlist' callback must be called after 'reset_commands_selector'
        # callback to ensure displaying the menu of the currently focused node.
        urwid.connect_signal(self, 'changed', partial(
            self.reset_commands_selectors.delay, duration=0.4))
        urwid.connect_signal(self, 'commandlist', partial(self.on_commandlist.delay, duration=0.5))

    @property
    def current_widget(self):
        try:
            return self.get_focus_widgets()[0]
        except IndexError:
            return None

    @property
    def current_node(self):
        wd = self.current_widget
        if wd is None:
            return None
        node = getattr(wd, 'node', None)
        if not node or set(node) == {'f'}:
            return None
        else:
            return node

    async def _wait(self, *args):
        position = self.get_focus()[-1]
        rev = getattr(self.current_widget, 'rev', None)
        if rev is None:
            return await super()._wait()
        # Maybe the current_node was obsoleted
        try:
            _rev = await process.hg_plain(
                'log', '--hidden', '--rev', f'last(allsuccessors({rev}))', '--template', '{rev}')
            if _rev:
                rev = _rev
        except OSError:
            # cwd was stripped. Doing more complicated stuff would be not useful.
            return await super()._wait()
        try:
            await asyncio.gather(
                super()._wait(),
                dialog.popup_processing(
                    self._on_focus_rev(rev),
                    'Searching for the previous changeset... Close this popup to cancel.'
                ))
        except mixin.NotFound:
            self.set_focus(position)

    async def _on_filter(self, *args):
        edit = widgets.edit(
            [('ui.label', 'revset: ')], self._changeset.rev or '')
        choice = await dialog.ask(edit, title='FILTER TREE', focus_content=True)
        if choice:
            self.reset_rev(edit.get_edit_text().strip() or None)

    def reset_rev(self, rev):
        """Reset the view with the given revision set."""
        self._changeset.rev = rev
        self.ensure()

    async def _on_focus_rev(self, rev, *args):
        """Set the focus focus to cset with the given `rev` (-1 == cwd)."""
        widget, position = await self._changeset.get_rev(rev)
        if position is not None:
            self.set_focus(position + len(self._cwd) + len(self._shelve))
            self._invalidate()

    def focus_p1(self):
        """Set focus on the first parent of the current cset."""
        widget, position = self.get_focus()
        if getattr(widget, 'p1', None) is None:
            return
        task = self.on_focus_rev.ensure(widget.p1)
        # delaying popup_processing prevents popup if the cset already fetched
        dialog.popup_processing.delay(task, duration=0.1)

    def focus_c1(self):
        """Set focus on the first child of the current cset."""
        widget, position = self.get_focus()
        if not getattr(widget, 'children', None) or not widget.children[0]:
            return
        task = self.on_focus_rev.ensure(widget.children[0])
        # delaying popup_processing prevents popup if the cset already fetched
        dialog.popup_processing.delay(task, duration=0.1)

    def set_focus(self, position, *args, **kwargs):
        super().set_focus(position, *args, **kwargs)
        urwid.emit_signal(self, 'changed')  # ensure other panes sync

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key is None:
            return None
        if self._command_map[key] == config.CMD_NEXT_RELATED:
            self.focus_p1()
            return
        if self._command_map[key] == config.CMD_PREV_RELATED:
            self.focus_c1()
            return
        return key


class patchlistwalker(_multiwalker):

    signals = ['jump_diff']

    def __init__(self):
        self.node = None
        self._summary = summarywalker()
        self._summaryextra = summaryextrawalker()
        self._description = descriptionwalker()
        self._diffstat = diffstatwalker()
        self._diff = diffwalker()
        super().__init__(
            [self._summary, self._summaryextra, self._description,
             self._diffstat, self._diff])
        urwid.connect_signal(
            self._diffstat, 'link',
            lambda *args: urwid.emit_signal(self, 'jump_diff', *args)
        )

    async def reset_node(self, node):
        await self.stop()
        self.node = node
        self._summary.node = node
        self._summaryextra.node = node
        self._description.node = node
        self._diffstat.node = node
        self._diff.node = node

    def get_diff_position(self):
        return self.startof(self._diff)

    def get_filtered_filename(self):
        return self._diff.filename

    def set_filtered_filename(self, filename):
        self._diff.filename = filename
        self._diffstat.filename = filename

    async def _wait(self):
        # Load task is specific order to ensure that prefered sections
        # appears quickly (PROCESSES_SEMAPHORE may delay a few of
        # them).
        await asyncio.gather(
            self._diff.wait(),
            self._summary.wait(),
            self._description.wait(),
            self._diffstat.wait(),
            self._summaryextra.wait(),
        )
        urwid.emit_signal(self, 'completed')


class patchlistbox(
        mixin.filterable_listbox,
        mixin.searchable_listbox, mixin.refreshable_listbox, _listbox):
    """Manage the patch content, a.k.a. summary and diff."""

    def __init__(self):
        self._search_pattern = ''
        self.on_jump_to_diffline = ensure_one(self._on_jump_to_diffline)
        self.on_filter = ensure_one(self._on_filter)
        super().__init__(patchlistwalker())

    def _connect_all(self):
        super()._connect_all()
        urwid.connect_signal(self, 'filter', self.on_filter.ensure)
        # TODO: do not access private attribute.
        urwid.signals.connect_signal(
            self.body, 'jump_diff', self.on_jump_to_diffline.ensure)
        urwid.signals.connect_signal(self, 'refresh', lambda *a: self.ensure())

    def change_focus(self, *args, **kwargs):
        # workaround urwid bug: just don't focus on selectable if we can't
        try:
            return super().change_focus(*args, **kwargs)
        except urwid.ListBoxError:
            pass

    async def reset_node(self, node):
        # resetonly if not CWD and changed. We always reset on cwd as
        # the user evently want to view changes while cset is expected
        # not to be modified outside the application.
        if node is not None and node == self.body.node:
            return
        await self.body.reset_node(node)
        self.ensure()

    def _iter_widgets(self, startpos=None, forward=True):
        pos = self.focus_position if startpos is None else startpos
        nextgetter = self.body.get_next if forward else self.body.get_prev
        widget = self.body[pos]
        while widget:
            yield widget, pos
            widget, pos = nextgetter(pos)

    def _goto(self, matcher, startpos=None, forward=True):
        for widget, pos in self._iter_widgets(startpos, forward):
            if matcher(widget, pos):
                self.set_focus(pos)
                self._invalidate()
                break

    async def _on_jump_to_diffline(self, fname, *args):
        assert self.wait.task
        await self.wait.task    # wait until all loaded
        self._goto(
            lambda w, p: fname in w.text,
            self.body.get_diff_position())

    async def _on_filter(self, *args):
        edit = widgets.edit(
            [('ui.label', 'file: ')], self.body.get_filtered_filename() or '')
        choice = await dialog.ask(edit, title='FILTER PATCH', focus_content=True)
        if choice:
            val = edit.get_edit_text().strip() or None
            self.body.set_filtered_filename(val)
            self.ensure()

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key is None:
            return
        command = self._command_map[key]
        if command in (config.CMD_PREV_RELATED, config.CMD_NEXT_RELATED):
            forward = command == config.CMD_NEXT_RELATED
            self._goto(
                lambda w, p: w.text.startswith(('diff --git', '@@ ')),
                startpos=self.focus_position + (1 if forward else -1),
                forward=forward,
            )
            return
        return key


class maincontroler(ensurable):

    def __init__(self, rev=None, hidden=False):
        self._graph = graphlistbox(rev=rev, hidden=hidden)
        self._patch = patchlistbox()
        self._grep_pattern = ''
        self.on_focus_patch = ensure_one(self._on_focus_patch)
        self.on_grep = ensure_one(self._on_grep)
        self._connect_all()

    def _connect_all(self):
        # Duration 300ms is arbitrary. It seems a good value on my
        # laptop with my usage. By this way I can repeatedly hit
        # down/up keys to search for a commit without firing the patch
        # subprocesses.
        urwid.signals.connect_signal(
            self._graph, 'changed', partial(self.on_focus_patch.delay, duration=0.1))

    def get_widget(self):
        return mainwidget.mainwidget(mainwidget.packer([
            mainwidget.pane(self._graph, 'TREE'),
            mainwidget.pane(self._patch, 'PATCH'),
        ]))

    async def _on_focus_patch(self, *args):
        await self._patch.reset_node(self._graph.current_node)

    def ensure(self):
        self._graph.ensure()
        self._patch.ensure()

    def cancel(self):
        self._graph.cancel()
        self._patch.cancel()

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key == '?':
            open_popup(dialog.simple(mainwidget.thehelp(), 'HELP'))
        elif key == 'G':
            self.on_grep.ensure()

    async def _on_grep(self, *args):
        edit = widgets.edit([('ui.label', 'pattern: ')], self._grep_pattern)
        answer = await dialog.ask(edit, title='Grep', focus_content=True)
        if not answer:
            return
        pattern = edit.get_edit_text()
        if pattern:
            revset = await dialog.popup_processing(self._grep_revset(pattern))
        else:
            revset = ''
        self._graph.reset_rev(revset)
        self._patch.search_pattern(pattern),

    async def _grep_revset(self, pattern):
        self._grep_pattern = pattern
        csets = defaultdict(set)
        with HG_SEMAPHORE:
            async for line in process.hg('grep', '--all', '-l', pattern):
                try:
                    data = dict(parse_colored_line(line))
                except ValueError:
                    pass
                csets[data['grep.rev']].add(data['grep.filename'])
        revset = ' or '.join(csets)
        return f'({revset})'

    def enable_commands(self):
        self._graph.connect_commands()


def filter_files(expression):
    regexp = re.compile(expression)
    paths = tuple(str(p) for p in Path('.').glob('**/*'))
    return (p for p in paths if regexp.match(p))

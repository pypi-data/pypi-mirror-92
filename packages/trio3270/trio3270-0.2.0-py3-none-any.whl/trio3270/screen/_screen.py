from __future__ import annotations

import abc
import collections
import itertools
import logging
import operator
from contextlib import asynccontextmanager
from typing import Optional, List, Tuple, Dict, Any, Union, Deque, AsyncContextManager, Sequence, Collection

import attr
import trio

import trio3270
from trio3270 import util as _util
from trio3270.screen.buffer import ScreenChar, ScreenBuffer


class AField(abc.ABC):
    @property
    @abc.abstractmethod
    def size(self): ...

    @abc.abstractmethod
    async def fill(self, connection: trio3270.IBM3270, data: str): ...


@attr.s(auto_attribs=True, frozen=True)
class Field(AField):
    row: int
    start_column: int
    end_column: int

    @property
    def size(self):
        return self.end_column - self.start_column

    async def fill(self, connection: trio3270.IBM3270, data: str):
        return await connection.send_string_at(
            self.row, self.start_column, data[:self.size].ljust(self.size))


@attr.s(init=False, auto_attribs=True, slots=True)
class _TextChecker:
    _item: Optional[Any]
    _args: Sequence[Any]
    _kwargs: Dict[str, Any]

    def __init__(self, *args, **kwargs):
        if args:
            self._item = args[0]
            args = args[1:]
        else:
            self._item = None
        self._args = args
        self._kwargs = kwargs

    def __getitem__(self, item):
        return _TextChecker(item, *self._args, **self._kwargs)

    def __call__(self, *args, **kwargs):
        return _TextChecker(self._item, *self._args, *args, **self._kwargs, **kwargs)

    def do_check(self, buffer: ScreenBuffer):
        if self._item is None:
            slices = (slice(None, None), slice(None, None))
        else:
            slices = _util._calc_slices(self._item)[:2]

        for line in buffer[slices]:
            text_line = ''.join(sc.char for sc in line)
            for pos, check in itertools.chain(enumerate(self._args, start=1), self._kwargs.items()):
                if isinstance(check, _TextChecker):
                    result = check.do_check(buffer)
                else:
                    result = check in text_line
                if result:
                    return pos
        return None


text = _TextChecker()


@attr.s(auto_attribs=True)
class CombinedField(AField):
    _fields: List[AField]

    @property
    def size(self):
        return sum(f.size for f in self._fields)

    async def fill(self, connection: trio3270.IBM3270, data: str):
        for f in self._fields:
            this, data = data[:f.size], data[f.size:]
            await f.fill(connection, data=this)
            if not data:
                break

    def __getitem__(self, item) -> AField:
        # can collapse to parent field
        fields = self._fields[item:]
        if len(fields) == 0:
            raise IndexError(f'{item} not found. Only {len(self._fields)} here.')
        elif len(fields) == 1:
            return fields[0]
        elif len(fields) == len(self._fields):
            return self
        else:
            return CombinedField(fields)


@attr.s(auto_attribs=True)
class Screen:
    connection: trio3270.IBM3270
    timeout: float = 1
    timeout_no_change: float = 3
    _min_wait: float = 0.35
    _settle_wait_time: float = 0.005
    logger: Optional[logging.Logger] = None
    entry_fields: List[Field] = attr.ib(init=False, factory=list, repr=False)
    fields: List[AField] = attr.ib(init=False, factory=list, repr=False)
    buffer: ScreenBuffer = attr.ib(init=False, default=None, repr=False)
    outputs: Dict[str, AField] = attr.ib(init=False, factory=dict, repr=False)
    row: _util.SubscriptionNamespace = attr.ib(init=False, repr=False, default=None)
    column: _util.SubscriptionNamespace = attr.ib(init=False, repr=False, default=None)
    label: _util.SubscriptionNamespace = attr.ib(init=False, repr=False, default=None)
    field: _util.SubscriptionNamespace = attr.ib(init=False, repr=False, default=None)
    _cleanups: Deque[str] = attr.ib(init=False, repr=False, factory=collections.deque)
    _command_cleanup: str = ''
    _last_logged_screen: Optional[ScreenBuffer] = attr.ib(init=False, repr=False, default=None)
    history: Optional[Deque[Tuple[str, tuple, dict, ScreenBuffer]]] = attr.ib(
        init=False, repr=False, factory=lambda: collections.deque(maxlen=5))

    def __attrs_post_init__(self):
        self.command_sent_no_change = None
        self.field = _util.SubscriptionNamespace(self.get_field)
        self.row = _util.SubscriptionNamespace(self.get_field_by_row)
        self.column = _util.SubscriptionNamespace(self.get_field_by_column)
        self.label = _util.SubscriptionNamespace(self.get_field_by_label)

    def check(self, *args, **kwds):
        """
        Happy path check
        """
        result = _TextChecker(None, *args, **kwds).do_check(self.buffer)
        if result is None:
            raise RuntimeError(f'Check failed {args} {kwds}')

    async def __aenter__(self):
        self._cleanups.append(self._command_cleanup)
        self._command_cleanup = ''
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._command_cleanup:
            if exc_type is not None:
                with trio.move_on_after(1) as teardown:
                    teardown.shield = True
                    if self.logger is not None:
                        self.logger.warning(f'Executing cleanup {self._command_cleanup!r} on exception {exc_val!r}',
                                            stacklevel=2)
                    await self.connection.send_string(self._command_cleanup)
            else:
                await self.connection.send_string(self._command_cleanup)
        self._command_cleanup = self._cleanups.popleft()

    def get_field_by_row(self, row_spec: int) -> CombinedField:
        """
        Returns fields using the row
        :param row_spec: A row number, related only to the rows with fields.
        :return: A `CombinedField` with all fields in that specific row.
        """
        rows = self._group_fields_by('row')
        return CombinedField(sorted(rows[row_spec], key=operator.attrgetter('start_column')))

    def get_field_by_column(self, column_spec: Union[str, int]) -> CombinedField:
        """
        Returns fields using the column.
        :param column_spec: Can be a column number or a column name.
        - If it is a number, it is related to the number of different columns with fields.
        - If it is a name, it is related to the label above the first field in the column.
        :return: A `CombinedField` with all the fields in the column
        """
        if isinstance(column_spec, int):
            columns = self._group_fields_by('start_column')
            return CombinedField(sorted(columns[column_spec], key=operator.attrgetter('row')))
        elif isinstance(column_spec, str):
            raise NotImplementedError('Field column label detection not implemented yet')
        raise TypeError(f'Unknown spec  {column_spec!r}')

    def _group_fields_by(self, group_attribute) -> List[List[Field]]:
        grouped = collections.defaultdict(list)
        for field in self.entry_fields:
            grouped[getattr(field, group_attribute)].append(field)
        grouped = [v for k, v in sorted(grouped.items())]
        return grouped

    def get_field_by_label(self, label: str) -> CombinedField:
        """
        :param label: A string with the name to search
        :return: A `CombinedField` with the field and all the following fields in the row that don't have a name
        """
        label = _util.normalize_identifier(label)
        for field in self.entry_fields:
            candidate_name = _util.normalize_identifier(
                self.buffer.get_str(field.row, column=0, end_column=field.start_column))
            if candidate_name and candidate_name.endswith(label):
                return CombinedField([f for f in self.entry_fields
                                      if f.row == field.row and f.start_column >= field.start_column])
        else:
            raise KeyError(f'Field with name {label!r} not found.')

    async def __call__(self, *args, **kwargs) -> Screen:
        # - no need to wait even without change: _min_wait=0
        # - need to wait when no change, and I want you to wait: _min_wait=X
        # - need to wait when no change, but I will wait it myself: _min_wait=None # DEFAULT
        # - need to wait when no change, but I will wait it myself, and the time to wait actually
        #   differs from the default: unsupported
        _min_wait = kwargs.pop('_min_wait', None)
        _check = kwargs.pop('_check', None)
        _cleanup = kwargs.pop('_cleanup', '')

        """Executes a command"""
        if len(args) == 0:
            command = trio3270.ENTER
        else:
            command, args = args[0], args[1:]
        kwfields = await self.wait(num_fields=len(args), field_names=kwargs)
        for n, data in enumerate(args):
            await self.fill(self.entry_fields[n], data)
        for name, data in kwargs.items():
            await self.fill(kwfields[name], data)
        # History save
        if self.history is not None:
            self.history.append((command, args, kwargs, await ScreenBuffer.from_connection(self.connection)))
        try:
            await self.connection.send_string(command)
            self._command_cleanup = _cleanup + self._command_cleanup
            if _min_wait is None:
                self.command_sent_no_change = trio.current_time() + self._min_wait
                await self.refresh_buffer()
            else:
                if _min_wait > 0:
                    self.command_sent_no_change = trio.current_time() + _min_wait
                    await self.wait()  # wait a change while refreshing....
                else:  # no need to wait, refresh now
                    await self.refresh_buffer(wait_settle=False)
                self.command_sent_no_change = None

            if _check is not None:
                self.check(_check)
            return self
        finally:
            self._log_command(command=command,
                              kwargs_text=','.join(f'{k}={v}' for k, v in kwargs.items()),
                              args_text=','.join(args),
                              stacklevel=2)

    def log_with_buffer(self, message, level=logging.DEBUG, stacklevel=1):
        """Avoid repetition by keeping the last logged screen"""
        if self.logger is None:
            return
        if self._last_logged_screen == self.buffer:
            self.logger.log(level, message, stacklevel=stacklevel + 1)
        else:
            _screen = self.buffer.serialize()
            self.logger.log(level, f'{message} {_screen.decode()}', stacklevel=stacklevel + 1)
            self._last_logged_screen = self.buffer

    def _log_command(self, command, kwargs_text, args_text, level=logging.DEBUG, stacklevel=2):
        if args_text:
            args_text += '|'
        if kwargs_text:
            kwargs_text += '|'
        self.log_with_buffer(f'[CMD] {args_text}{kwargs_text}{command}', level=level, stacklevel=stacklevel + 1)

    async def wait(self, *checks: Sequence[Union[_TextChecker, str]], num_fields: int = 0,
                   field_names: Collection[str] = ()):
        """
        Will wait until the screen changed, or something expected happens.
        If the screen didn't change, it will still wait min_wait.
        """
        wait_attempt = 0
        error = RuntimeError('Unknown error')
        _timeout = self.timeout if self.command_sent_no_change is None else self.timeout_no_change
        with trio.move_on_after(_timeout):
            while True:
                for check in checks:
                    if not isinstance(check, _TextChecker):
                        check = _TextChecker(None, check)
                    if not check.do_check(self.buffer):
                        error = RuntimeError('Failed check')
                        break
                else:
                    if num_fields > len(self.entry_fields):
                        error = IndexError(f'Not enough positional fields (got {len(self.entry_fields)})')
                    else:
                        try:
                            kwarg_fields = {}
                            for field_name in field_names:
                                field = self.label[field_name]
                                kwarg_fields[field_name] = field
                        except KeyError as e:
                            error = e
                        else:
                            error = None
                if error is None:
                    if self.command_sent_no_change is None:
                        return kwarg_fields
                    # no error but no change could mean the screen didn't change yet.
                    # We wait *at least* `min_wait`
                    minimum_wait_needed = self.command_sent_no_change - trio.current_time()
                    if minimum_wait_needed > 0:
                        wait_time = max(min(0.1 + 2 ** wait_attempt * 0.05, 0.5), minimum_wait_needed)
                    else:  # no more wait needed so just accept this
                        return kwarg_fields
                else:
                    wait_time = min(0.1 + 2 ** wait_attempt * 0.05, 0.5)
                await trio.sleep(wait_time)
                await self.refresh_buffer()
                wait_attempt += 1
        # noinspection PyUnreachableCode
        raise error

    async def refresh_buffer(self, wait_settle: bool = True):
        while True:
            old_buffer, self.buffer = self.buffer, await ScreenBuffer.from_connection(self.connection)
            if old_buffer is None or old_buffer.find_diff(self.buffer) is None:
                break  # no difference or no previous buffer; just accept it
            self.command_sent_no_change = None  # mark that a change was found
            if not wait_settle:
                break
            await trio.sleep(self._settle_wait_time)  # change found. wait for it to settle.
        self.refresh_fields()
        return self.buffer

    def refresh_fields(self):
        self.entry_fields = []
        self.fields = []
        for row_no in range(self.buffer.lines):
            for is_protected, _chars in itertools.groupby(enumerate(self.buffer[row_no]),
                                                          key=lambda _sc: 'protected' in _sc[1].attribs):
                if not is_protected:
                    _chars: List[Tuple[int, ScreenChar]] = list(_chars)
                    field = Field(row_no, _chars[0][0], _chars[-1][0] + 1)
                    self.entry_fields.append(field)

        self.fields = [CombinedField(self.entry_fields[:n]) for n in range(len(self.entry_fields) - 1)]
        self.fields.extend(self.entry_fields[-1:])

    async def fill(self, field: AField, data):
        await field.fill(self.connection, data)

    def __getitem__(self, item):
        if self.command_sent_no_change is not None:
            minimum_wait_needed = self.command_sent_no_change - trio.current_time()
            if minimum_wait_needed > 0:
                raise RuntimeError('A command was sent but no change was detected. '
                                   f'You must wait {minimum_wait_needed:.2f}s and refresh the buffer.')
            else:
                raise RuntimeError('A command was sent but no change was detected. '
                                   f'You must refresh the buffer.')
        rows, cols, rows_as_list, _ign = _util._calc_slices(item)
        result = self.buffer[item]
        if rows_as_list:
            return [''.join(sc.char for sc in result_line) for result_line in result]
        else:
            return ''.join(sc.char for sc in result)

    def get_field(self, field_spec: Any) -> Union[Field, CombinedField]:
        """
        :param field_spec:
         - str - tries label row first, then label column
         - int - row number
         - tuple - gets a specific field in a combined field
        :return:
        """
        continuation = None
        if isinstance(field_spec, tuple):
            field_spec, continuation = field_spec[0], field_spec[1:]
            if len(continuation) == 1:
                continuation = continuation[0]
        for attempt in (self.label, self.row):
            try:
                field = attempt[field_spec]
            except (KeyError, IndexError):
                continue
            else:
                if continuation is not None:
                    field = field[continuation]
                return field
        raise KeyError(f'Field not found {field_spec!r}')


@asynccontextmanager
async def connect(*args, **kwds) -> AsyncContextManager[Screen]:
    params_screen = {name: kwds.pop(name) for name in ['min_wait', 'timeout', 'timeout_no_change',
                                                       'settle_wait_time', 'logger'] if name in kwds}
    kwds.setdefault('use_delay', False)
    async with trio3270.IBM3270(*args, **kwds) as conn:
        async with Screen(conn, **params_screen) as s:
            yield s

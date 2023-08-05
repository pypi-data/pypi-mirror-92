from __future__ import annotations

import base64
import json
import zlib
from typing import FrozenSet, Optional, Set, List, Union, Tuple

import attr

import trio3270
from trio3270 import util

_format_codes = {
    'c0': {
        0xc0: set(),
        0xc1: {'modified'},
        0xc4: {'detectable'},
        0xc8: {'intensified'},
        0xc9: {'intensified', 'modified'},
        0xcc: {'non-display'},
        0xcd: {'non-display', 'modified'},
        0xe0: {'protected'},
        0xe1: {'protected', 'modified'},
        0xe8: {'protected', 'intensified'},
        0xec: {'protected', 'non-display', 'modified'},
        0xd0: {'numeric'},
        0xd1: {'numeric', 'modified'},
        0xd8: {'numeric', 'intensified'},
        0xd9: {'numeric', 'intensified', 'modified'},
        0xf0: {'protected', 'numeric'},
        0xf1: {'protected', 'numeric', 'modified'},
        0xf8: {'protected', 'numeric', 'intensified'},
        0xfc: {'protected', 'numeric', 'non_display'},
        0xfd: {'protected', 'numeric', 'non_display', 'modified'},
    },
    '41': {
        0xf1: {'blink'},
        0xf2: {'reverse'},
        0xf4: {'underscore'},
        0xf8: {'intensify'},
    },
    '42': {
        0xf0: {'neutral black'},
        0xf1: {'blue'},
        0xf2: {'red'},
        0xf3: {'pink'},
        0xf4: {'green'},
        0xf5: {'turquoise'},
        0xf6: {'yellow'},
        0xf7: {'neutral white'},
        0xf8: {'black'},
        0xf9: {'deep blue'},
        0xfa: {'orange'},
        0xfb: {'purple'},
        0xfc: {'pale green'},
        0xfd: {'pale turquoise'},
        0xfe: {'grey'},
        0xff: {'white'},
    },
    '43': {
        0xf0: {'default'},
        0xf1: {'APL'},
        0xf8: {'DBCS'},
    }
}


@attr.s(auto_attribs=True, frozen=True)
class ScreenChar:
    char: str
    attribs: FrozenSet[str]

    @classmethod
    def fromtext(cls, text: str, old_attribs: Optional[Set[str]] = None):
        if old_attribs is None:
            old_attribs = {'protected'}
        attribs = old_attribs.copy()
        char = ' '
        if len(text) == 2:
            char_ord = int(text, 16)
            if char_ord not in [0, 32]:
                char = chr(char_ord)
            elif 'underscore' in attribs:
                char = '_'
            else:
                char = ' '
        elif len(text) == 4 and text.startswith('c3'):
            char = chr(int(text[-2:], 16) + 0x40)
        elif text.startswith(('SF(', 'SA(')):
            old_attribs.add('protected')
            attribs = set()
            for param in text[3:-1].split(','):
                format_code, _sep, data = param.partition('=')
                try:
                    attribs.update(_format_codes[format_code][int(data, 16)])
                except KeyError as e:
                    raise TypeError(f'Unknown format code {format_code!r} {data!r}') from e
        else:
            raise TypeError(f'** Unknown code {text!r}')
        if text.startswith('SA('):
            return None, attribs
        else:
            return cls(char, frozenset(old_attribs)), attribs


@attr.s(auto_attribs=True)
class ScreenBuffer:
    screencap: List[str] = attr.ib(repr=False)
    _buffer: List[List[ScreenChar]] = attr.ib(init=False, default=None, repr=False)

    @classmethod
    def from_serialized_bytes(cls, payload: bytes) -> ScreenBuffer:
        return cls(json.loads(zlib.decompress(base64.a85decode(payload, foldspaces=True)).decode('ascii')))

    def serialize(self) -> bytes:
        payload = zlib.compress(json.dumps(self.screencap, separators=(',', ':')).encode('ascii'), 9)
        return base64.a85encode(payload, foldspaces=True).strip()

    @property
    def lines(self) -> int:
        return len(self.screencap)

    def columns(self) -> int:
        return max(len(x) for x in self._buffer)

    def __attrs_post_init__(self):
        self._buffer = []
        for line in self.screencap:
            chars = line.strip().split()
            screen_line = []
            attribs = None
            for char in chars:
                try:
                    screen_char, attribs = ScreenChar.fromtext(char, attribs)
                except TypeError as e:
                    self._buffer.append(screen_line)
                    raise TypeError(f'Error generating screen: {self}') from e
                if screen_char is not None:
                    screen_line.append(screen_char)
            self._buffer.append(screen_line)

    def __getitem__(self, item) -> Union[ScreenChar, List[ScreenChar], List[List[ScreenChar]]]:
        rows, cols, rows_as_list, cols_as_list = util._calc_slices(item)
        result = []
        for nrow in range(*rows.indices(len(self._buffer))):
            _screen_row = self._buffer[nrow]
            if cols_as_list:
                result.append([_screen_row[ncol] for ncol in range(*cols.indices(len(_screen_row)))])
            else:
                result.append(_screen_row[cols.start])
        if not rows_as_list:
            result = result[-1]
        return result

    def get_str(self, row: int, column: int = 0, end_column: int = None) -> str:
        return self.get_list(start_row=row, start_column=column, end_column=end_column)[0]

    def get_list(self, start_row: int, end_row: int = None, start_column: int = 0,
                 end_column: int = None) -> List[str]:
        if end_row is None:
            end_row = start_row + 1
        slices = (slice(start_row, end_row), slice(start_column, end_column))
        return [''.join(sc.char for sc in result_line) for result_line in self[slices]]

    def find_diff(self, other: ScreenBuffer) -> Optional[Tuple[int, int]]:
        for nrow, row in enumerate(self._buffer):
            for ncol, sc in enumerate(row):
                if 'protected' not in sc.attribs:
                    continue
                if sc != other[nrow, ncol]:
                    return nrow, ncol
        return None

    def __str__(self):
        return '\n'.join(self.get_list(0, len(self._buffer)))

    @classmethod
    async def from_connection(cls, connection: trio3270.IBM3270) -> ScreenBuffer:
        return ScreenBuffer(await connection('ReadBuffer', 'Ascii'))

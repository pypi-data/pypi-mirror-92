import re
import unicodedata
from typing import Any, Callable

import attr


@attr.s
class LineReader:
    stream = attr.ib()
    max_line_length = attr.ib(type=int, default=16384)

    def __attrs_post_init__(self):
        self._line_generator = self.generate_lines(self.max_line_length)

    @staticmethod
    def generate_lines(max_line_length):
        buf = bytearray()
        find_start = 0
        while True:
            newline_idx = buf.find(b'\n', find_start)
            if newline_idx < 0:
                # no b'\n' found in buf
                if len(buf) > max_line_length:
                    raise ValueError("line too long")
                # next time, start the search where this one left off
                find_start = len(buf)
                more_data = yield
            else:
                # b'\n' found in buf so return the line and move up buf
                line = buf[:newline_idx + 1]
                # Update the buffer in place, to take advantage of bytearray's
                # optimized delete-from-beginning feature.
                del buf[:newline_idx + 1]
                # next time, start the search from the beginning
                find_start = 0
                more_data = yield line

            if more_data is not None:
                buf += bytes(more_data)

    async def readline(self):
        line = next(self._line_generator)
        while line is None:
            more_data = await self.stream.receive_some(1024)
            if not more_data:
                return b''  # this is the EOF indication expected by my caller
            line = self._line_generator.send(more_data)
        return line


def quote_param(param):
    param = str(param)
    param = ' '.join(param.splitlines()).replace('"', r'\u0022')
    if any(char in param for char in ' ,()'):
        param = f'"{param}"'
    return param


def tobool(true_value=None, false_value=None):
    def _booleanator(value):
        if value == true_value or (true_value is None and value != false_value):
            return True
        elif false_value is None or value == false_value:
            return False
        else:
            return None

    return _booleanator


def _calc_slices(item):
    """
        e[10] -> linha 10 inteira, string
        e[...,10] -> coluna 10 inteira, lista
        e[10:15] -> linhas 10 a 15 inteiras, lista
        e[10,10] -> Caracter exato em 10,10, string
        e[10,10:] -> linha 10, coluna 10 ate o fim da linha, string
        e[10,10:15] -> linha 10, coluna 10 ate 15, string
        e[10:15,10:15] -> regiao quadrada de 10,10 ate 15,15, lista
        """
    if isinstance(item, tuple):
        rows = item[0]
        cols = item[1]
    else:
        rows = item
        cols = None
    if rows is Ellipsis:
        rows = slice(None, None, None)
    if cols is Ellipsis or cols is None:
        cols = slice(None, None, None)
    if not isinstance(rows, slice):
        endrow = rows + 1
        if not endrow:
            endrow = None  # -2:-1 is a correct slice for rows = -2; but -1:0 is empty so we specialcase
        rows = slice(rows, endrow, None)
        rows_as_list = False
    else:
        rows_as_list = True
    if not isinstance(cols, slice):
        endcol = cols + 1
        if not endcol:
            endcol = None
        cols = slice(cols, endcol, None)
        cols_as_list = False
    else:
        cols_as_list = True
    return rows, cols, rows_as_list, cols_as_list


@attr.s(auto_attribs=True)
class SubscriptionNamespace:
    method_to_call: Callable[[Any], Any]

    def __getitem__(self, item: Any) -> Any:
        return self.method_to_call(item)


def normalize_identifier(source_text: str) -> str:
    # replace all accents by the non-combining version
    source_text = "".join([c for c in unicodedata.normalize('NFKD', source_text) if not unicodedata.combining(c)])
    # replace special chars and spaces with underlines, consolidates them and strips around.
    source_text = re.sub(r'[^a-zA-Z0-9]+', '_', source_text).strip('_')
    # casefolds
    source_text = source_text.casefold()
    return source_text

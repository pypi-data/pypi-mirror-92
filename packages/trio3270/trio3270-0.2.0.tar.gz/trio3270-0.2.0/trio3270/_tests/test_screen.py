import collections

import pytest
import trio

from trio3270 import HOST_WAIT, PF12
from trio3270._tests import _samples as samples
from trio3270.screen import Screen


class MockConnection:
    def __init__(self, *screens, auto_advance=True):
        self.num_reads = 0
        self.sent = collections.deque()
        self._screens = collections.deque(screens)
        self._auto_advance = auto_advance

    async def send_string(self, *strings):
        return await self.send_string_at(None, None, *strings)

    async def send_string_at(self, row, column, *strings):
        text = ''.join(strings)
        self.sent.append((row, column, text))
        if self._auto_advance and any(ch in text for ch in HOST_WAIT):
            self.advance()

    async def __call__(self, command, *args, **kwargs):
        if command.casefold() == 'readbuffer' and args[0].casefold() == 'ascii':
            self.num_reads += 1
            return self._screens[0]

    def advance(self):
        self._screens.popleft()


async def test_screen(autojump_clock):
    c = MockConnection(samples.caixa_network_start_screen, samples.sicmn_login_screen)
    s = Screen(c)
    await s.refresh_buffer()
    assert s[16, 15:24] == 'SELECIONE'
    assert len(s.entry_fields) == 2
    assert s.entry_fields == s.label['opcao']._fields
    assert s.field['opcao'] == s.label['opcao']
    assert s.field['opcao', 1] == s.entry_fields[1]
    await s(opcao='466')
    assert list(c.sent) == [(16, 37, '4'), (16, 40, '66'), (None, None, r'\n')]
    c.sent.clear()
    with pytest.raises(KeyError):
        x = s.label['opcao']
    assert s.field['usuario'][0] == s.entry_fields[0]
    assert s.field['senha'][0] == s.entry_fields[1]
    assert s.column[0][3] == s.entry_fields[3]


async def test_buffer_refresh(autojump_clock):
    c = MockConnection(samples.caixa_network_start_screen, samples.sicmn_login_screen, auto_advance=False)
    s = Screen(c)
    await s.refresh_buffer()
    await s(opcao='466')
    c.num_reads = 0
    t = trio.current_time()
    with pytest.raises(KeyError):
        await s(usuario='c056091', senha='XXXX')
    assert trio.current_time() - t == 3
    c.advance()
    await s(usuario='c056091', senha='XXXX')
    assert list(c.sent) == [(16, 37, '4'), (16, 40, '66'), (None, None, r'\n'),
                            (15, 18, 'c056091 '), (17, 18, 'XXXX    '), (None, None, r'\n')]


async def test_delay_login_screen(autojump_clock):
    c = MockConnection(samples.caixa_network_start_screen, samples.sicmn_login_screen, auto_advance=False)
    s = Screen(c)
    await s.refresh_buffer()
    await s(opcao='466')
    t = trio.current_time()
    async with trio.open_nursery() as nursery:
        @nursery.start_soon
        async def advance_to_login_screen():
            await trio.sleep(0.35)
            c.advance()
        await s(usuario='c056091', senha='XXXX')
    assert list(c.sent) == [(16, 37, '4'), (16, 40, '66'), (None, None, r'\n'),
                            (15, 18, 'c056091 '), (17, 18, 'XXXX    '), (None, None, r'\n')]


async def test_column_number():
    c = MockConnection(samples.simcn_edit_screen, auto_advance=False)
    s = Screen(c)
    await s.refresh_buffer()
    # print(s.buffer)
    assert len(s.column[0]._fields) == 9
    # assert len(s.column['valor']) == 9


async def test_teardown():
    c = MockConnection(samples.caixa_network_start_screen, samples.sicmn_login_screen, samples.simcn_start_screen,
                       auto_advance=True)
    s = Screen(c)
    await s.refresh_buffer()
    async with s:
        await s(opcao='466', _cleanup=PF12)
        await s()
    assert c.sent[-1][-1] == PF12


async def test_wait_check():
    c = MockConnection(samples.sicmn_login_screen, samples.simcn_start_screen,
                       auto_advance=True)
    s = Screen(c)
    await s.refresh_buffer()
    async with s:
        await s()
        await s.wait('Menu Principal')

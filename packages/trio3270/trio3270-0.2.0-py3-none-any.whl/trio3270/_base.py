import os
import random
import subprocess
import sys
import typing as t

import trio
import attr
import tricycle

from . import util
from .util import _calc_slices

FROZEN = getattr(sys, 'frozen', False)

if FROZEN:
    EXE_PATH = os.path.dirname(sys.executable)
    SCRIPT_PATH = getattr(sys, '_MEIPASS', EXE_PATH)
else:
    SCRIPT_PATH = os.path.dirname(__file__)
    EXE_PATH = SCRIPT_PATH


class IBM3270Error(Exception):
    pass


class IBM3270CommandError(IBM3270Error):
    pass


@attr.s(slots=True)
class IBM3270Status:
    kbd = attr.ib(type=str, default='')
    fmt = attr.ib(type=bool, converter=util.tobool('F'), default=False)
    prot = attr.ib(type=bool, converter=util.tobool('P'), default=False)
    conn = attr.ib(type=str, default='')
    emu = attr.ib(type=str, default='')
    model = attr.ib(type=int, converter=int, default=0)
    rows = attr.ib(type=int, converter=int, default=0)
    cols = attr.ib(type=int, converter=int, default=0)
    row = attr.ib(type=int, converter=int, default=0)
    col = attr.ib(type=int, converter=int, default=0)
    window = attr.ib(type=int, converter=lambda wid: int(wid, 16), default='0')
    time = attr.ib(default=None)


@attr.s(auto_attribs=True)
class IBM3270(tricycle.ScopedObject):
    host: str
    port: int
    _model: int = 3
    _logical_units: t.Optional[t.Sequence[str]] = None
    passthru: bool = False
    extended_data_stream: bool = False
    tn3270e: bool = True
    use_ssl: bool = True
    _window: bool = False
    scriptport: t.Optional[int] = None
    use_delay: bool = True
    _p: t.Optional[trio.Process] = attr.ib(init=False, default=None, repr=False)
    status: IBM3270Status = attr.Factory(IBM3270Status)
    _linereader: util.LineReader = attr.ib(init=False, default=None, repr=False)
    _command_lock: trio.Lock = attr.ib(init=False, factory=trio.Lock, repr=False)

    def __attrs_post_init__(self):
        if self.scriptport is None:
            self.scriptport = random.randint(10000, 50000)

    async def __open__(self):
        await self.connect()

    async def __close__(self):
        await self.close()

    async def connect(self) -> trio.Process:
        if self._p is not None and self._p.returncode is None:
            return self._p

        conn = []
        if self.passthru:
            conn.append('P:')
        if self.extended_data_stream:
            conn.append('S:')
        if not self.tn3270e:
            conn.append('N:')
        if self.use_ssl:
            conn.append('L:')
        host = f'[{self.host}]:{self.port}'
        if self._logical_units:
            host = f"{','.join(self._logical_units)}@{host}"
        conn.append(host)
        conn = ''.join(conn)

        if sys.platform == 'win32':
            self._p = await self._connect_windows(conn)
        else:
            self._p = await self._connect_linux(conn)
        self._linereader = util.LineReader(self._p.stdout)
        await self._update_status()
        await self("Wait", '3270Mode')
        return self._p

    async def _connect_linux(self, hostname: str) -> trio.Process:
        if self._window:
            cmd = ['x3270', '-script']
        else:
            cmd = ['s3270', '-utf8', '-set', 'blankFill']
            if self.use_delay:
                cmd.extend(['-xrm', 's3270.unlockDelay: true'])
        if self._model != 4:
            cmd.extend(['-model', str(self._model)])
        if self._window:
            cmd.append('-once')

        cmd.extend(['-noverifycert', hostname])
        return await trio.open_process(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            close_fds=True,
        )

    async def _connect_windows(self, hostname: str) -> trio.Process:
        if self._window:
            cmd = [
                os.path.join(SCRIPT_PATH, 'data', 'wc3270.exe'),
                '-scriptport', str(self.scriptport), '-scriptportonce',
            ]
        else:
            cmd = [os.path.join(SCRIPT_PATH, 'data', 'ws3270.exe'), '-utf8', '-set', 'blankFill']
            if self.use_delay:
                cmd.extend(['-xrm', 'ws3270.unlockDelay: true'])
            # else:
            #     cmd.extend(['-xrm', 'ws3270.unlockDelay: false',
            #                 '-xrm', 'ws3270.unlockDelayMs: 0'])

        cmd.extend(['-model', str(self._model), hostname, '-noverifycert'])
        cmd.append('-utf8')
        if self._window:
            # try:
            #     await trio.run_process('mode con: cols=80 lines=32', shell=True)
            # except subprocess.CalledProcessError:
            #     pass
            self._p2 = await trio.open_process(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                close_fds=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            await trio.sleep(1)  # espera a conexao
            cmd = [
                os.path.join(SCRIPT_PATH, 'data', 'x3270if.exe'),
                '-t', str(self.scriptport),
                '-i',
            ]
        info = subprocess.STARTUPINFO()
        info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = 0  # SW_HIDE
        return await trio.open_process(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=info,
        )

    async def _send_command(self, command, *args) -> t.List[str]:
        if args:
            args = ', '.join(util.quote_param(arg) for arg in args)
            command = f"{command}({args})\n"
        else:
            command = f"{command}\n"

        async with self._command_lock:
#            print(f"Sending: {command!r}")
            await self._p.stdin.send_all(command.encode('utf-8'))
            result = []
            while True:
                line = await self._linereader.readline()
#                print(f"GOT: {line!r}")
                if not line:
                    # TODO: Correct exception
                    raise IBM3270Error("Disconnected")
                line = line.decode('utf-8').rstrip('\r\n')
                if line.startswith('data: '):
                    result.append(line[6:])
                else:
                    result.append(line)
                    if line in ('ok', 'error'):
                        break
        self.status = IBM3270Status(*result[-2].split())
        if result[-1] == "ok":
            return result[:-2]
        else:
            e = IBM3270CommandError(f"Error executing {command}!", command, '\n'.join(result[:-2]))
            raise e

    async def __call__(self, command: str, *args, **kwds) -> t.List[str]:
#        print("Call", command, args, kwds)
        if command.lower() == 'transfer' and not kwds:
            raise TypeError(f"Transfer command needs arguments as keywords")
        if kwds:
            if command.lower() != 'transfer':
                raise TypeError(f"Command {command!r} does not accept keyword arguments {kwds}")
            if args:
                raise TypeError(f"Transfer command needs all arguments as keywords")
            if any(kwd not in kwds for kwd in ('HostFile', 'LocalFile')):
                raise TypeError(f"Transfer command requires `HostFile` and `LocalFile` keyword arguments")
            args = tuple(f"{k}={v}" for k, v in kwds.items())
        return await self._send_command(command, *args)

    async def _update_status(self):
        await self('')

    _replace_map = {
        '\b': '\\b',
        '\n': '\\n',
        '\f': '\\f',
        '\r': '\\r',
        '\t': '\\t',
    }

    async def send_string(self, *strings: str) -> None:
        r"""
            \b		Left
            \f		Clear*
            \n		Enter*
            \pan	PA(n)*
            \pfnn	PF(nn)*
            \r		Newline
            \t		Tab
            \T		BackTab
        """
        # Falta tratar:
        # \exxxx EBCDIC  character in hex
        # \uxxxx Unicode character in hex
        # \xxxxx Unicode character in hex
        for string in strings:
            for ch, replacement in self._replace_map.items():
                string = string.replace(ch, replacement)
            await self('String', string)

    async def send_string_at(self, row: int, col: int, *strings: str) -> None:
        await self.set_position(row, col)
        if not self.can_write:
            await self('Tab')
            if not self.can_write or self.status.row != row:
                raise IBM3270Error(f"Linha {row} não possui campo após coluna {col}")
        return await self.send_string(*strings)

    @property
    def can_write(self) -> bool:
        return (self.status.conn and  # connected
                self.status.kbd == 'U' and  # unlocked
                not self.status.prot)  # not protected

    async def set_position(self, new_row: int, new_col: int) -> None:
        if not 0 <= new_col < self.status.cols:
            raise ValueError(f'Col number out of range: 0 <= {new_col} < {self.status.cols}')
        if not 0 <= new_row < self.status.rows:
            raise ValueError(f'Row number out of range: 0 <= {new_row} < {self.status.rows}')
        await self('MoveCursor', new_row, new_col)

    def __getitem__(self, item) -> t.Coroutine:
        rows, cols, result_as_list, _ign = _calc_slices(item)
        return self.get(rows, cols, as_list=result_as_list)

    async def get(self, row_slice: slice, col_slice: slice, as_list: bool = False) -> t.Union[list, str]:
        colstart, colstop, step = col_slice.indices(self.status.cols)
        rowstart, rowstop, step = row_slice.indices(self.status.rows)
#        print(f'POS: {rowstart}:{rowstop},{colstart}:{colstop}')
        result = await self('Ascii', rowstart, colstart,
                            abs(rowstop - rowstart), abs(colstop - colstart))
        if as_list:
            return result
        else:
            return '\n'.join(result)

    async def paginador(self, lin_ini: int, lin_fim: int, col_ini: int, col_fim: int,
                        func_acabou_pre: t.Callable = None,
                        func_acabou_pos: t.Callable = None,
                        npags_lado: int = 1, tecla_prox: int = 8, tecla_dir: int = 11,
                        tecla_esq: int = 10) -> t.Generator[str, None, None]:
        """
            Paginador de captura de texto via IBM
            :Parameters:
             `lin_ini`: linha inicial
             `lin_fim`: linha final
             `col_ini`: coluna inicial
             `col_fim`: coluna final
             `func_acabou_pre` : testa (antes da captura da tela) se é a última página
             `func_acabou_pos` : testa (depois da captura da tela) se é a última página
             `npags_lado` : número de páginas laterais para compor toda a tabela
             `tecla_prox` : passar para a próxima página (padrão PF8)
             `tecla_dir`  : passar para a tela da direita -->  (padrão PF11)
             `tecla_esq`  : voltar para a tela da esquerda <-- (padrão PF10)
        """
        tecla = tecla_dir
        while True:
            if func_acabou_pre and await func_acabou_pre(self):
                break
            listas = [await self[lin_ini:lin_fim, col_ini:col_fim]]
            for x in range(npags_lado - 1):
                await self('PF', tecla)
                listas.append(await self[lin_ini:lin_fim, col_ini:col_fim])
            if tecla == tecla_dir:
                tecla = tecla_esq
            else:
                tecla = tecla_dir
                listas.reverse()
            for i, texts in enumerate(zip(*listas)):
                yield f'{i:02d} {" ".join(texts)}'
            if func_acabou_pos and await func_acabou_pos(self):
                break
            await self('PF', tecla_prox)

    async def pf(self, number: int) -> None:
        await self('PF', number)

    async def close(self) -> None:
        try:
            if self._p is not None:
                await self('Quit')
                self._p.kill()
                await self._p.wait()
        except IBM3270Error:
            pass

    async def receive_file(self, filename: str, destination: str, **kwds) -> t.List[str]:
        kwargs = {
            'HostFile': filename,
            'LocalFile': destination,
            'Exist': 'replace',
        }
        kwargs.update(kwds)
        result = await self('Transfer', **kwargs)
        return result

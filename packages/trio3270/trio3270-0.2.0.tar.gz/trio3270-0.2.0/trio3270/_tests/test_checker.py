from trio3270._tests import _samples as samples
from trio3270.screen._screen import text
from trio3270.screen.buffer import ScreenBuffer


def test_text_checker():
    t = text[5]
    b = ScreenBuffer(samples.caixa_network_start_screen)
    assert text('SELECIONE').do_check(buffer=b)
    assert text[4]('Tecle').do_check(buffer=b)
    assert not text[5]('Tecle').do_check(buffer=b)

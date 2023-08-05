from trio3270._tests import _samples as samples
from trio3270.screen.buffer import ScreenBuffer


def test_load_buffer():
    b1 = ScreenBuffer(samples.caixa_network_start_screen)
    assert b1.get_str(8, 9, 32) == 'CAIXA ECONÔMICA FEDERAL'
    sc = b1[8, 9]
    assert sc.char == 'C'
    assert 'protected' in sc.attribs
    sc = b1[16, 37]
    assert 'protected' not in sc.attribs


def test_compare_buffer():
    b1 = ScreenBuffer(samples.caixa_network_start_screen)
    b2 = ScreenBuffer(samples.caixa_network_start_screen)
    assert b1 == b2
    b3 = ScreenBuffer(samples.sicmn_login_screen)
    assert b1 != b3


def test_find_diff_protected_only():
    b1 = ScreenBuffer(samples.simcn_34)
    screen_jp_patched = samples.sicmn_34_ja_preenchida.copy()
    screen_jp_patched[1] = samples.simcn_34[1]  # patch time in the screen to match
    screen_jp_patched[5] = samples.simcn_34[5]  # patch reret which is not a field
    b2 = ScreenBuffer(screen_jp_patched)
    assert b1 != b2
    assert b1.find_diff(b2) is None


def test_serialization():
    b1 = ScreenBuffer(samples.caixa_network_start_screen)
    b2 = ScreenBuffer.from_serialized_bytes(b1.serialize())
    assert b1 == b2
    assert b1.screencap == b2.screencap

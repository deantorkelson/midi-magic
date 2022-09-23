import pytest

from ..util.helpers import find_instrument_program, velocity_from_name, get_pitch, pitch_step_generator, key_mod_for_pitch


@pytest.mark.parametrize("clef,key,steps_from_top,expected_pitch", [
    ('&', 'C', 0, 89),  # F5
    ('&', 'B', 5, 82),  # A#2
    ('&', 'G', 3, 84),  # C5
    ('F', 'C', 0, 69),  # A3
    ('F', 'Db', 6, 58),  # Bb2
    ('F', 'Eb', 2, 65),  # F3
])
def test_get_pitch(clef, key, steps_from_top, expected_pitch):
    assert get_pitch(clef, key, steps_from_top) == expected_pitch


def test_find_instrument_program():
    assert find_instrument_program('distortion_guitar') == 30
    assert find_instrument_program('piccolo') == 72
    

def test_velocity_from_name():
    assert velocity_from_name('ppp') == 10
    assert velocity_from_name('ff') == 95


def test_pitch_iter():
    pitch = 84
    pitch_gen = pitch_step_generator(1)
    for _ in range(7):
        step = next(pitch_gen)
        pitch -= step
    assert pitch == 72
    pitch_gen = pitch_step_generator(5)
    for _ in range(7):
        step = next(pitch_gen)
        pitch -= step
    assert pitch == 60


def test_key_mod_for_pitch():
    b_maj_key_mods = [1, 1, 0, 1, 1, 1, 0]
    d_pitch = 62
    assert key_mod_for_pitch(b_maj_key_mods, d_pitch) == 1
    b_pitch = 107
    assert key_mod_for_pitch(b_maj_key_mods, b_pitch) == 0

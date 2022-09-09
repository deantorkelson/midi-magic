import pytest

from helpers.helpers import find_instrument_program, velocity_from_name, is_note, is_rest, get_pitch, get_duration


@pytest.mark.parametrize("clef,key,steps_from_top,expected_pitch", [
    ('&', 'C', 0, 89),  # F5
    ('&', 'B', 5, 82),  # A#2
    ('F', 'C', 0, 69),  # A3
    ('F', 'Db', 6, 58),  # Bb2
])
def test_get_pitch(clef, key, steps_from_top, expected_pitch):
    assert get_pitch(clef, key, steps_from_top) == expected_pitch

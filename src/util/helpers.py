import json
import logging
from collections.abc import Generator

NAME_TO_VELOCITY = {
    'ppp': 10,
    'pp': 30,
    'p': 40,
    'mp': 50,
    'mf': 65,
    'f': 80,
    'ff': 95,
    'fff': 110
}

MAJOR_KEY_PITCH_MODIFIERS = {
    #     C  D  E  F  G  A  B
    'C': [0, 0, 0, 0, 0, 0, 0],
    'G': [0, 0, 0, 1, 0, 0, 0],
    'D': [1, 0, 0, 1, 0, 0, 0],
    'A': [1, 0, 0, 1, 1, 0, 0],
    'E': [1, 1, 0, 1, 1, 0, 0],
    'B': [1, 1, 0, 1, 1, 1, 0],
    'F#': [1, 1, 1, 1, 1, 1, 0],
    'C#': [1, 1, 1, 1, 1, 1, 1],
    'Cb': [-1, -1, -1, -1, -1, -1, -1],
    'Gb': [-1, -1, -1, 0, -1, -1, -1],
    'Db': [0, -1, -1, 0, -1, -1, -1],
    'Ab': [0, -1, -1, 0, 0, -1, -1],
    'Eb': [0, 0, -1, 0, 0, -1, -1],
    'Bb': [0, 0, -1, 0, 0, 0, -1],
    'F': [0, 0, 0, 0, 0, 0, -1]
}


def find_instrument_program(instrument_name: str) -> int:
    programs = open('src/util/instrument_programs.json', 'r')
    data = json.load(programs)
    return data[instrument_name]


def velocity_from_name(name: str) -> int:
    return NAME_TO_VELOCITY[name]


def is_note(char: str) -> bool:
    note_characters = 'whqex'
    return char in note_characters


def is_rest(char: str) -> bool:
    rest_characters = 'WHQEX'
    return char in rest_characters


# Returns duration of note in quarter notes
def get_duration(char: str) -> float:
    if char in 'Ww':
        return 4
    if char in 'Hh':
        return 2
    if char in 'Qq':
        return 1
    if char in 'Ee':
        return 0.5
    if char in 'Xx':
        return 0.25


def key_mod_for_pitch(key_pitch_mods, pitch) -> int:
    octave_pitch = (pitch % 12)
    index = octave_pitch - (octave_pitch // 2)
    # octave pitches  c = 0, d = 2, e = 4, f = 5, g = 7, a = 9, b = 11
    # desired pitches c = 0, d = 1, e = 2, f = 3, g = 4, a = 5, b = 6
    # logging.debug(f"{pitch} -> {octave_pitch} -> {index}")
    return key_pitch_mods[index]


def pitch_step_generator(index: int) -> Generator[int, None, None]:
    # pitches contains the number of semitones req'd to go from one note to the next
    #        C->D->E->F->G->A->B->C
    pitches = [2, 2, 1, 2, 2, 2, 1]
    while True:
        yield pitches[index % 7]
        index -= 1


def get_pitch(clef: str, key: str, steps_from_top: int) -> int:
    assert clef in 'F&'
    if clef == '&':
        top_line_pitch = 89  # MIDI number for F5
        pitch_start_index = 2
    else:
        top_line_pitch = 69  # MIDI number for A3
        pitch_start_index = 4
    unkeyed_note_pitch = top_line_pitch
    pitch_gen = pitch_step_generator(pitch_start_index)
    for _ in range(steps_from_top):
        unkeyed_note_pitch -= next(pitch_gen)
    key_pitch_mods = MAJOR_KEY_PITCH_MODIFIERS[key]
    keyed_note_pitch = unkeyed_note_pitch + key_mod_for_pitch(key_pitch_mods, unkeyed_note_pitch)
    return keyed_note_pitch

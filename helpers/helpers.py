import json
import logging

# 10  30 40 50 65 80 95 110
# ppp pp p  mp mf f  ff fff
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

# call a key's array and pass in index of note, modify pitch by its value
# so if something is in C major,
MAJOR_KEY_PITCH_MODIFIERS = {
    #     A  B  C  D  E  F  G
    'C': [0, 0, 0, 0, 0, 0, 0],
    'G': [0, 0, 0, 0, 0, 1, 0],
    'D': [0, 0, 1, 0, 0, 1, 0],
    'A': [0, 0, 1, 0, 0, 1, 1],
    'E': [0, 0, 1, 1, 0, 1, 1],
    'B': [1, 0, 1, 1, 0, 1, 1],
    'F#': [1, 0, 1, 1, 1, 1, 1],
    'C#': [1, 1, 1, 1, 1, 1, 1],
    'Cb': [-1, -1, -1, -1, -1, -1, -1],
    'Gb': [-1, -1, -1, -1, -1, 0, -1],
    'Db': [-1, -1, 0, -1, -1, 0, -1],
    'Ab': [-1, -1, 0, -1, -1, 0, 0],
    'Eb': [-1, -1, 0, 0, -1, 0, 0],
    'Bb': [0, -1, 0, 0, -1, 0, 0],
    'F': [0, -1, 0, 0, 0, 0, 0],
}


def find_instrument_program(instrument_name: str) -> int:
    programs = open('helpers/instrument_programs.json', 'r')
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


def pitch_iterator(index: int) -> int:
    # pitches contains the number of semitones req'd to go from one note to the next
    #        G->A->B->C->D->E->F->G
    pitches = [2, 2, 1, 2, 2, 1, 2]
    yield pitches[index % 7]
    index += 1


# C-2 is pitch 0, +1 for each half step up
def get_pitch(clef: str, key: str, steps_from_top: int) -> int:
    assert clef in 'F&'
    if clef == '&':
        top_line_pitch = 89  # MIDI number for F5
    else:
        top_line_pitch = 69  # MIDI number for A3
    unkeyed_note_pitch = top_line_pitch
    for _ in range(steps_from_top):
        unkeyed_note_pitch -= pitch_iterator()
    # problem - this note pitch is wrong. consider an A4 (num 81) in the key of C, treble clef
    # distance from top is 3
    # problem is that not every step down from the top is equal to one midi pitch num down
    # idea: knowing that treble starts on F and bass starts on A, maybe make a generator that allows
    #   you to iterate through the unkeyed pitches of the clef, then modify with key as needed?

    return 65

import json


def find_instrument_program(instrument_name: str) -> int:
    programs = open('helpers/instrument_programs.json', 'r')
    data = json.load(programs)
    return data[instrument_name]


def velocity_from_name(name: str) -> int:
    # todo
    return 50


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


def get_pitch(clef: str, key: str, distance_from_top: int) -> int:
    return 65

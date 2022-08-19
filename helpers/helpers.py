import json


def find_instrument_program(instrument_name: str):
    programs = open('helpers/instrument_programs.json', 'r')
    data = json.load(programs)
    return data[instrument_name]


def velocity_from_name(name: str):
    # todo
    return 50

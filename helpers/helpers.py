import json


def find_instrument_program(instrument_name):
    programs = open('helpers/instrument_programs.json', 'r')
    data = json.load(programs)
    return data[instrument_name]

import os
from midiutil import MIDIFile
from helpers.helpers import find_instrument_program


class MidiMagic:
    def __init__(self, song_dir):
        self.song_dir = song_dir

    def create_midi(self):
        song_files = os.listdir(f"songs/{self.song_dir}")
        num_channels = len(song_files) - 1
        print(song_files)
        midi = MIDIFile(1)
        track = 0
        for file_name in song_files:
            time = 0
            if file_name == 'meta.txt':
                continue
            instrument = file_name.split('.')[0]
            # lookup instrument program number
            midi.addTrackName(track, 0, instrument)
            midi.addProgramChange(track, track, 0, find_instrument_program(instrument))
            file = open(f"songs/{self.song_dir}/{file_name}", "r")
            lines = file.readlines()
            num_lines = len(lines)
            line_index = 0
            done_reading_file = False
            while not done_reading_file:
                measure = []
            track += 1
        with open("generated_midi/test.mid", "wb") as output_file:
            midi.writeFile(output_file)
        print('done')


        # read in the entire file with readlines
        # iterate through and grab the current measure
        #   do this by going from start (init to 0) up to but not including the next line that starts with a number
        # once all the lines are collected
        # read in metadata (clef, dynamics, etc.)
        # read the measure from left to right
        # if a note is encountered
        #   add it to the midi file
        #   at the end of reading that column, increase `time` based on the largest note encountered

    def read_next_measure(self, lines) -> list[list[str]]:
        # self.line_index doesn't make sense - should make a new MidiFile class or something
        # that handles reading in each of the files
        measure = []
        new_measure_found = False
        while line_index < num_lines and not new_measure_found:
            if not lines[line_index].strip()[0].isdigit():
                # not in a new measure, add the line to the measure we're looking at and keep going
                measure.append(lines[line_index])
                line_index += 1
            else:
                # new measure found, stop reading and parse the previous measure
                new_measure_found = True
        return ''


magic = MidiMagic('the-lick')
magic.create_midi()

import os
from midiutil import MIDIFile
from helpers.helpers import find_instrument_program


class MidiMagicFile:
    def __init__(self, song_dir, file_name, midi):
        self.song_dir: str = song_dir
        self.file_name: str = file_name
        self.midi: MIDIFile = midi
        self.line_index: int = 0

    # processes the MidiMagic text file into midi on the given track
    def process_to_track(self, track):
        instrument: str = self.file_name.split('.')[0]
        # lookup instrument program number
        self.midi.addTrackName(track, 0, instrument)
        self.midi.addProgramChange(track, track, 0, find_instrument_program(instrument))
        file = open(f"songs/{self.song_dir}/{self.file_name}", "r")
        lines: list[str] = file.readlines()
        done_reading_file = False
        # process each measure
        while not done_reading_file:
            measure = self.read_in_next_measure(lines)
            if len(measure) == 0:
                done_reading_file = True
                continue
            self.measure_to_midi(measure)


    def measure_to_midi(self, measure):
        # read in metadata (clef, dynamics, etc.)
        # read the measure from left to right
        # if a note is encountered
        #   add it to the midi file
        #   at the end of reading that column, increase `time` based on the largest note encountered
        return

    def read_in_next_measure(self, lines) -> list[str]:
        measure = []
        num_lines = len(lines)
        new_measure_found = False
        while self.line_index < num_lines and not new_measure_found:
            if not lines[self.line_index].strip()[0].isdigit():
                # not in a new measure, add the line to the measure we're looking at and keep going
                measure.append(lines[self.line_index])
                self.line_index += 1
            else:
                # new measure found, stop reading and parse the previous measure
                new_measure_found = True
        return measure

class MidiMagic:
    def __init__(self, song_dir):
        self.song_dir = song_dir

    def create_midi(self):
        song_files = os.listdir(f"songs/{self.song_dir}")
        print(song_files)
        midi = MIDIFile(1)
        track = 0
        for file_name in song_files:
            time = 0
            if file_name == 'meta.txt':
                continue
            MidiMagicFile(self.song_dir, file_name, midi).process_to_track(track)
            track += 1
        with open("generated_midi/test.mid", "wb") as output_file:
            midi.writeFile(output_file)
        print('done')


magic = MidiMagic('the-lick')
magic.create_midi()

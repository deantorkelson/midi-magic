import os
from midiutil import MIDIFile
from helpers.helpers import find_instrument_program, velocity_from_name

# consts
CRESCENDO = 'c'
DECRESCENDO = 'd'


class MidiMagicFile:

    def __init__(self, song_dir, file_name, midi):
        self.song_dir: str = song_dir
        self.file_name: str = file_name
        self.midi: MIDIFile = midi
        self.line_index: int = 0
        self.velocity = 50

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

    def measure_to_midi(self, measure: list[str]):
        print(measure)
        measure_key: str = measure[0].split()[1]
        measure.pop(0)
        dynamics: str = measure[-1]
        velocity_modifier: str = ''

        if dynamics[0] != '|':
            # we have dynamics
            measure.pop()
            dynamics_split = dynamics.split()
            sign = dynamics_split[0]
            if dynamics_split[0][0].isalpha():
                # starting velocity
                self.velocity = velocity_from_name(dynamics_split[0])
                sign = dynamics_split[1]
            if sign == '<':
                velocity_modifier = CRESCENDO
            elif sign == '>':
                velocity_modifier = DECRESCENDO
        print(measure)
        # index as we read measure from left to right
        index: int = 0

        # read the measure from left to right
        # if a note is encountered
        #   add it to the midi file
        #   at the end of reading that column, increase `time` based on the largest (smalled?) note encountered
        return

    def read_in_next_measure(self, lines) -> list[str]:
        measure = []
        num_lines = len(lines)
        new_measure_found = False
        while self.line_index < num_lines and not new_measure_found:
            # read in THIS line
            # if next line starts with a number, we're done
            line = lines[self.line_index]
            if line != '\n':
                measure.append(line)
            if self.line_index + 1 < num_lines:
                nextLine: str = lines[self.line_index + 1].strip()
                if len(nextLine) > 0 and nextLine[0].isdigit():
                    # new measure found, stop reading and parse the previous measure
                    new_measure_found = True
            self.line_index += 1
        return measure

class MidiMagic:
    def __init__(self, song_dir):
        self.song_dir = song_dir

    def create_midi(self):
        song_files = os.listdir(f"songs/{self.song_dir}")
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

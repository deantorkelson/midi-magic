import os
import logging
import sys
from midiutil import MIDIFile
from helpers.helpers import find_instrument_program, velocity_from_name, is_note, is_rest, get_pitch, get_duration

# consts
CRESCENDO = 'c'
DECRESCENDO = 'd'


class MidiMagicFile:
    def __init__(self, song_dir, file_name, midi, key):
        self.song_dir: str = song_dir
        self.file_name: str = file_name
        self.midi: MIDIFile = midi
        self.key = key
        self.line_index: int = 0
        self.velocity = 50
        self.time = 0

    # processes the MidiMagic text file into midi on the given track
    def process_to_track(self, track: int):
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
            self.measure_to_midi(measure, track)

    def update_velocity(self, velocity_modifier):
        if velocity_modifier == CRESCENDO:
            self.velocity += 1
        elif velocity_modifier == DECRESCENDO:
            self.velocity -= 1

    def measure_to_midi(self, measure: list[str], track: int):
        print(measure)
        try:
            # TODO: if key is minor get relative major
            key = measure[0].split()[1]
        except IndexError:
            key = self.key
        measure.pop(0)
        dynamics: str = measure[-1]
        clef: str = ''
        velocity_modifier = CRESCENDO
        for line in measure:
            char = line[0]
            if char != '|':
                if char == 'F' or char == '&':
                    clef = char
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
        print(*measure)
        # index as we read measure from left to right. start at 1 to account for vertical bars
        lr_index: int = 1

        # read the measure from left to right
        done = False
        while not done:
            done = True
            # this value is in quarter notes, can be fractional (hopefully)
            time_step = 117
            for vert_index, line in enumerate(measure):
                if lr_index >= len(line):
                    continue
                done = False  # if any line still has something left, keep going
                char = line[lr_index]
                duration = get_duration(char)
                if is_note(char):
                    # look up its pitch using key, clef, and line index
                    # todo need to change once ledger lines are supported
                    pitch = get_pitch(clef, key, vert_index)
                    #   look up its duration based on the note
                    self.midi.addNote(self, track, pitch, self.time, duration, self.velocity)
                    if duration < time_step:
                        time_step = duration
                elif is_rest(char):
                    # update time step to value of rest
                    time_step = duration
                elif char not in "- ":
                    logging.warning(f"Invalid character detected in measure, line {vert_index} pos {lr_index}: {char}")
            self.update_velocity(velocity_modifier)
            self.time += time_step
            lr_index += 1
        # at the end of reading the column, increase `time` based on the smallest note encountered
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
                next_line: str = lines[self.line_index + 1].strip()
                if len(next_line) > 0 and next_line[0].isdigit():
                    # new measure found, stop reading and parse the previous measure
                    new_measure_found = True
            self.line_index += 1
        return measure

class MidiMagic:
    def __init__(self, song_dir):
        self.song_dir = song_dir
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def create_midi(self):
        song_files = os.listdir(f"songs/{self.song_dir}")
        midi = MIDIFile(1)
        track: int = 0
        key = 'C'
        for file_name in song_files:
            if file_name == 'meta.txt':
                # get metadata, like key
                # TODO need to get metadata first
                continue
            MidiMagicFile(self.song_dir, file_name, midi, key).process_to_track(track)
            print(track)
            track += 1
        with open("generated_midi/test.mid", "wb") as output_file:
            midi.writeFile(output_file)
        print('done')


magic = MidiMagic('the-lick')
magic.create_midi()

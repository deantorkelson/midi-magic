import os
import logging
import sys
import math
import re
from midiutil import MIDIFile
from util.helpers import find_instrument_program, velocity_from_name, is_note, is_rest, get_pitch, get_duration

# consts
CRESCENDO = 'c'
DECRESCENDO = 'd'
VEL_MODIFIER_AMOUNT = 4
DEFAULT_KEY = 'C'
OCTAVE_MOD = 1  # For some reason, instruments all sound really high. This is used to mellow things out a bit


class MidiMagicFile:
    def __init__(self, song_dir, file_name, midi, key):
        self.song_dir: str = song_dir
        self.file_name: str = file_name
        self.midi: MIDIFile = midi
        self.key = key
        self.line_index: int = 0
        self.velocity = velocity_from_name('mf')
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

    def update_velocity(self, velocity_modifier, time_step):
        velocity_delta = (VEL_MODIFIER_AMOUNT * math.ceil(time_step))
        if velocity_modifier == CRESCENDO:
            logging.debug(f"crescending by {velocity_delta}")
            self.velocity += velocity_delta
        elif velocity_modifier == DECRESCENDO:
            self.velocity -= velocity_delta

    def get_clef(self, measure):
        for line in measure:
            char = line[0]
            if char != '|' and (char == 'F' or char == '&'):
                return char

    def get_velocity_modifier(self, measure):
        dynamics: str = measure[-1].strip(" \n")
        if dynamics[0] != '|':
            sign = re.search('[<>]', dynamics)
            velocity_name = re.search('[pmf]+', dynamics, flags=re.IGNORECASE)
            logging.debug(f"sign: {sign and sign.group(0)}. velocity: {velocity_name and velocity_name.group(0)}")
            if velocity_name:
                self.velocity = velocity_from_name(velocity_name.group(0))
            if sign:
                if sign.group(0) == '<':
                    return CRESCENDO
                if sign.group(0) == '>':
                    return DECRESCENDO

    # This method returns the duration of the character, or time_step if it doesn't have a duration (e.g. '-' or ' ')
    def process_char(self, char, clef, key, vert_index, track, time_step) -> float:
        duration = get_duration(char)
        if is_note(char):
            pitch = get_pitch(clef, key, vert_index)
            logging.debug(f"adding note on track {track}, pitch {pitch}, time {self.time}, dur {duration}, vel {self.velocity}")
            self.midi.addNote(track, track, pitch-(OCTAVE_MOD * 12), self.time, duration, self.velocity)
            logging.debug(f"processing {char}. time_step: {time_step}, duration: {duration}")
            if duration < time_step or time_step == 0:
                logging.debug(f"returning duration of {duration}")
                return duration
        elif is_rest(char):
            # update time step to value of rest
            logging.debug(f"resting for {duration} beats")
            return duration
        return time_step

    def measure_to_midi(self, measure: list[str], track: int):
        try:
            # TODO: if key is minor get relative major
            key = measure[0].split()[1]
        except IndexError:
            key = self.key
        measure.pop(0)
        clef: str = self.get_clef(measure)
        velocity_modifier = self.get_velocity_modifier(measure)

        # index as we read measure from left to right. start at 1 to account for vertical bars
        lr_index: int = 1
        done = False
        while not done:
            done = True
            time_step = 0  # this value is in quarter notes, can be fractional
            for vert_index, line in enumerate(measure):
                if lr_index >= len(line):
                    continue
                done = False  # if any line still has something left, keep going
                char = line[lr_index]
                time_step = self.process_char(char, clef, key, vert_index, track, time_step)

            self.update_velocity(velocity_modifier, time_step)
            self.time += time_step
            logging.debug(f"new time, updated by {time_step}: {self.time}")
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
    def __init__(self, song_dir, log_level=logging.WARNING):
        self.song_dir = song_dir
        logging.basicConfig(stream=sys.stderr, level=log_level)

    def create_midi(self):
        song_files = os.listdir(f"songs/{self.song_dir}")
        midi = MIDIFile(1)
        track: int = 0
        for file_name in song_files:
            if file_name == 'meta.txt':
                continue  # do nothing, this is just for notes
            MidiMagicFile(self.song_dir, file_name, midi, DEFAULT_KEY).process_to_track(track)
            track += 1
        with open(f"generated_midi/{self.song_dir}.mid", "wb") as output_file:
            midi.writeFile(output_file)
        print('done')


def main():
    try:
        song_dir = sys.argv[1]
    except IndexError:
        song_dir = 'generic-pop-chords'
    log_level = None
    if len(sys.argv) > 1:
        args = " ".join(sys.argv[1:])
        if '-d' in args:
            log_level = logging.DEBUG
    magic = MidiMagic(song_dir, log_level)
    magic.create_midi()


if __name__ == "__main__":
    main()

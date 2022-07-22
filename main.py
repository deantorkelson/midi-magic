import os
from midiutil import MIDIFile
from helpers.helpers import find_instrument_program


def main():
    song_dir = 'the-lick'  # input('Which directory in `songs/` do you want to midi-fy?\n')
    song_files = os.listdir(f"songs/{song_dir}")
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
        file = open(f"songs/{song_dir}/{file_name}", "r")
        print(file.readlines())
        # read in the entire file with readlines
        # iterate through and grab the current measure
        #   do this by going from start (init to 0) up to but not including the next line that starts with a number
        # once all the lines are collected
        # read in metadata (clef, dynamics, etc.)
        # read the measure from left to right
        # if a note is encountered
        #   add it to the midi file
        #   at the end of reading that column, increase `time` based on the largest note encountered
        track += 1
    with open("generated_midi/test.mid", "wb") as output_file:
        midi.writeFile(output_file)
    print('done')


main()

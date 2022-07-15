import os
from midiutil import MIDIFile

def main():
    # prompt user for directory of song
    # read in number of files
    # number of channels == number of files - 1
    # for each non-meta.txt file
    #   set channel program (instrument) based on filename
    #   for each measure
    #   read it in
    song_dir = 'the-lick' # input('Which directory in `songs/` do you want to midi-fy?\n')
    song_files = os.listdir(f"songs/{song_dir}")
    num_channels = len(song_files) - 1
    print(song_files)
    midi = MIDIFile(1)
    time = 0
    track = 0
    midi.addNote(track, track, 40, 0, 1, 100)
    for file in song_files:
        if file == 'meta.txt':
            break
        instrument = file.split('.')[0]
        # lookup instrument program number
        midi.addTrackName(track, 0, instrument)
    with open("generated_midi/test.mid", "wb") as output_file:
        midi.writeFile(output_file)
    print('done')


main()

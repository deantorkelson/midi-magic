# Overview

## File Structure
### General
MIDIMAGIC songs should each have their own folder in the "songs/" directory, structured like this:
```
songs/
|-- song1/
    |-- meta.txt
    |-- lead_3_calliope.txt
    |-- synth_bass_1.txt
|-- song2/
    |-- distortion_guitar.txt
```
### meta.txt
This is an optional file, and just includes general information about the song (author, contributor, description, anything you want)

### <instrument_name>.txt
This file will contain the actual musical score in MIDIMAGIC format for a specified instrument.
See `src/util/instrument_programs.json` for a list of valid instrument names.


## Notation guide
### Measures
Measures are a series of 9 vertical pipes with a series of hyphens extending out every other line.
The measure number appears right above the top pipe, and the key for that measure is right after the
measure number (e.g. F#m for F sharp minor, or Bb for B flat major).

### Clefs
Clefs are positioned in the center of the vertical bars that denote the start of a measure
`&`: Treble clef
`F`: Bass clef

### Notes
`w`: whole note
`h`: half note
`q`: quarter note
`e`: eighth note
`x`: sixteenth note

### Rests
`W`: whole rest
`H`: half rest
`Q`: quarter rest
`E`: eighth rest
`X`: sixteenth rest

### Dynamics
ppp, pp, p, mp, mf, f, ff, fff all supported
`<`: cresendo
`>`: decrescendo
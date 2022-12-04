#!/usr/bin/env python3

from mido import MidiFile
import wordninja

# Read separate tracks
mid = MidiFile('song.mid')
track_notes = [[], []]
for i, track in enumerate(mid.tracks):
    for msg in track:
        if msg.type == 'note_off':
            track_notes[i-1].append((msg.note, msg.time))


def decode(key, track_num):
    # The key for track 1 is sorted sum of note/time to alphabet with q removed and j moved to its place
    letters = list(key)
    sorted_sums = sorted(set(sum((note, time)) for (note, time) in track_notes[track_num]))
    lookup = dict(zip(sorted_sums, letters))
    message = ""
    for note in track_notes[track_num]:
        message += lookup[sum(note)]
    split = ' '.join(wordninja.split(message))
    print(f"Track {track_num}: key => {key}")
    print(f"Track {track_num}: msg => {message}")
    print(f"Track {track_num}: split => {split}")
    return message

decode(key="abcdefghiklmnopqrstuvwxyz", track_num=0)
decode(key="abcdefghijklmnoprstuvwy", track_num=1)


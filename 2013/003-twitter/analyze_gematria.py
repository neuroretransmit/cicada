#!/usr/bin/env python3

lookup = {
    'F': 2,
    'U': 3,
    'TH': 5,
    'O': 7,
    'R': 11,
    'C': 13,
    'K': 13,
    'G': 17,
    'W': 19,
    'H': 23,
    'N': 29,
    'I': 31,
    'J': 37,
    'EO': 41,
    'P': 43,
    'X': 47,
    'S': 53,
    'Z': 53,
    'T': 59,
    'B': 61,
    'E': 67,
    'M': 71,
    'L': 73,
    'NG': 79,
    'ING': 79,
    'OE': 83,
    'D': 89,
    'A': 97,
    'AE': 101,
    'Y': 103,
    'IA': 107,
    'IO': 107,
    'EA': 109
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = ''
for k in lookup.keys():
    letters += k
letters = set(letters)
for letter in alphabet:
    if letter not in letters:
        print(letter)


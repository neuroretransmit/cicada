#!/usr/bin/env python3

""" 
SPECIAL SYMBOLS IN RUNES
:  == trip reset of supplied key (Welcome page has hard resets on F while skipping most of the first three lines)
.  == period
-  == word separator
-/ == word continuation on next line
&  == section separator
"""

import string
from pprint import pprint as pp

# Formatted in atbash per the Warning page
RUNE_LOOKUP = {
    'ᛠ': ['F'],
    'ᛯ': ['U'],
    'ᚣ': ['TH'],
    'ᚫ': ['O'],
    'ᚪ': ['R'],
    'ᛞ': ['C', 'K'],
    'ᛟ': ['G'],
    'ᛝ': ['W'],
    'ᛚ': ['H'],
    'ᛗ': ['N'],
    'ᛖ': ['I'],
    'ᛒ': ['J'],
    'ᛏ': ['EO'], 
    'ᛋ': ['P'], 
    'ᛉ': ['X'], 
    'ᛈ': ['S', 'Z'],
    'ᛇ': ['T'], 
    'ᛄ': ['B'], 
    'ᛁ': ['E'], 
    'ᚾ': ['M'], 
    'ᚻ': ['L'], 
    'ᚹ': ['NG', 'ING'], 
    'ᚷ': ['OE'], 
    'ᚳ': ['D'], 
    'ᚱ': ['A'],
    'ᚩ': ['AE'],
    'ᚦ': ['Y'],
    'ᚢ': ['IO', 'IA'],
    'ᚠ': ['EA'],
}

class Gematria:
    @staticmethod
    def substitution(mode=None, key=None):
        print("MODE:", mode)
        lookup = {}
        if mode == None:
            for k, v in zip(reversed(RUNE_LOOKUP.keys()), RUNE_LOOKUP.values()):
                lookup[k] = v
            pp(lookup)
            return lookup
        elif mode == "atbash":
            pp(RUNE_LOOKUP)
            return RUNE_LOOKUP
            return lookup
        elif mode == "vigenere":
            for k, v in zip(reversed(RUNE_LOOKUP.keys()), RUNE_LOOKUP.values()):
                lookup[k] = v
            return lookup
        else:
            raise NotImplementedError

    @staticmethod
    def preprocess_runes(txt, keep_tabs_breaks = True):
        preprocessed = txt.upper()
        if not keep_tabs_breaks:
            processed = txt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        # Repos like idkfa use the right rune, i opted for the left
        preprocessed = preprocessed.replace("ᛡ", "ᛯ")
        return preprocessed

    # TODO: Optimize out of O(scary) using tiered map lookups
    # TODO: Thread/yield and massive join for permutations
    """
    Convert runes to english text and filters results with impossible bigrams

    @txt  Runes to decrypt
    @mode Mode specifies the year i.e. 2013 is exactly as the Gematria Appears 
          in the picture, 2014 is with reversed keys (decryption fro warning page).
    @fast Flag to only use the first of multi-character entries and generate one
          result (TODO: change to int and specify the number of permutations)
    @overrides Overrides for multi-characters if better plaintext is seen in permutations
               this will limit the number of results.
    """
    @staticmethod
    def rune_to_english(txt, mode=None, fast=True, overrides = {}, key=None):
        txt = Gematria.preprocess_runes(txt, keep_tabs_breaks=True)
        lookup = Gematria.substitution(mode=mode, key=key)
        results = ['']
        impossible_bigrams = ["JQ", "QG", "QK", "QY", "QZ", "WQ", "WZ"]
        txt = Gematria.preprocess_runes(txt, keep_tabs_breaks=True)
        lookup_keys = list(lookup.keys())
        print(lookup)
        ki = 0 # key index
        kd = 0
        for n, c in enumerate(txt):
            if c in lookup:
                shift = 0
                if key:
                    shift = key[ki % len(key)]
                if fast:
                    for i in range(len(results)):
                        if c in overrides and n > 0 and txt[n-1] == ':':
                            shift = 0
                            ki -= 1
                        results[i] += lookup[lookup_keys[(lookup_keys.index(c) + shift) % len(lookup_keys)]][0]
                else:
                    candidates = lookup[lookup_keys[(lookup_keys.index(c) + shift) % len(lookup_keys)]]
                    stash = []
                    if len(candidates) > 1:
                        stash += stash
                    # Already figured out from list of results, explicitly set and skip O(scary)
                    if c in overrides:
                        if n > 0 and txt[n-1] == ':':
                            shift = 0
                            ki -= 1
                        for i in range(len(results)):
                            results[i] += overrides[c]
                        continue
                    for candidate in candidates:
                        working = results
                        queued_deletion = []
                        for i in range(len(working)):
                            # filter impossible bigrams
                            # see if if previous letter + candidate are in impossible bigrams
                            if working[i] and working[i][-1] + candidate[0] in impossible_bigrams:
                                queued_deletion.appened(i)
                                continue
                            if c in lookup: # FIXME: redundant yet necessary - give better check
                                
                                working[i] += candidate
                                break
                        for i in queued_deletion:
                            working.pop(i)
                        stash += working
                    results = stash
                ki += 1
            else:
                for i, result in enumerate(results):
                    # Only let whitespace, punctuation and digits through - print others
                    if c in " \t\n" or c in string.punctuation.replace(":", "") or c in string.digits:
                        results[i] += c
                    else:
                        print(c)
        return results

if __name__ == "__main__":
    import sys
    with open("03.jpg.runes.txt", "r") as runes, open("03.jpg.runes-possibilities.txt", "w") as three:
        data = runes.read()
        results = Gematria.rune_to_english(data, mode="vigenere", key=[6, 19, 28, 19, 20, 19, 13, 3], fast=True, overrides={'ᚠ': 'F'})
        for result in results:
            three.write(result + "\n")
    with open("04.jpg.runes.txt", "r") as runes, open("04.jpg.runes-possibilities.txt", "w") as four:
        data = runes.read()
        results = Gematria.rune_to_english(data, fast=True, overrides={'ᛝ': 'ING'})
        for result in results:
            four.write(result + "\n")
    

#!/usr/bin/env python3

""" 
SPECIAL SYMBOLS IN RUNES
:  == trip skip of supplied key (Welcome page has hard skips on F and continuing on next char,
      while skipping most of the first three lines)
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
    'ᛡ': ['U'],
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
    # TODO: Hard convert V to U (add to processing method)
    @staticmethod
    def key_to_shifts(key, mode=None, doubles=False):
        """ Convert text key to shifts
        @key     Key as string to turn into lookup shifts
        @mode    Mode to retrieve lookup table in
        @doubles Use double character lookups (i.e. use two letters for TH rather than the TH rune)
        """
        if isinstance(key, str):
            lookup = Gematria.substitution(mode=mode)
            lookup_vals = list(lookup.values())[::-1]
            shifts = []
            for i, c in enumerate(key):
                lookup_idx = 0
                for v in lookup_vals:
                    before = len(shifts)
                    peek = key[i+1] if i + 1 < len(key) and doubles else None
                    for p in v:
                        #print(lookup_idx, c, peek, p, lookup_idx)
                        if peek and c + peek == p:
                            # print(p)
                            shifts.append(lookup_idx + 1)
                        elif c == p:
                            # print(p)
                            shifts.append(lookup_idx + 1)
                        elif c == ' ':
                            # print(p)
                            shifts.append(0)
                    if before < len(shifts):
                        break
                    lookup_idx += 1
            return shifts

    @staticmethod
    def substitution(mode=None):
        """ Rearrange lookup table
        @mode Rearrangement mode {None, "atbash" (reversed), "vigenere" (same as None)}
        """
        print("MODE:", mode)
        if mode == None:
            lookup = {}
            for k, v in zip(reversed(RUNE_LOOKUP.keys()), RUNE_LOOKUP.values()):
                lookup[k] = v
            pp(lookup)
            return lookup
        elif mode == "atbash":
            pp(RUNE_LOOKUP)
            return RUNE_LOOKUP
        elif mode == "vigenere":
            return Gematria.substitution(mode=None)
        else:
            raise NotImplementedError

    @staticmethod
    def preprocess_runes(txt, keep_tabs_breaks = True):
        """ Correct/deal with whitespace (correction replaces my incorrect rune choice from font with 
            public transcriptions like idkfa)
        @txt              Text to process
        @keep_tabs_breaks Flag to remove whitespace or not
        """
        preprocessed = txt.upper()
        if not keep_tabs_breaks:
            processed = txt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        return preprocessed

    # TODO: Optimize out of O(scary) using tiered map lookups
    # TODO: Thread/yield and massive join for permutations
    # TODO: Work out of file or database to reduce RAM usage. Page 03.jpg eats all 32GB :(
    @staticmethod
    def rune_to_english(txt, mode=None, fast=True, overrides = {}, key=None, filter_impossible=True, rot=None):
        """ Convert runes to english text and filters results with impossible bigrams
        @txt               Runes to decrypt
        @mode              Encryption mode (specifies ordering of rune lookups: atbash, vigenere (same as None))
        @fast              Flag to only use the first of multi-character entries to limit to first result
        @overrides         Overrides for multi-characters if better plaintext is seen in permutations
        @key               Key for encryption method (currently only Vigenere)
        @filter_impossible Delete permutations containing bigrams that don't exist in english 
                           (not useful for tor URLs/hashes)
        """
        txt = Gematria.preprocess_runes(txt, keep_tabs_breaks=True)
        lookup = Gematria.substitution(mode=mode)
        results = ['']
        impossible_bigrams = ["JQ", "QG", "QK", "QY", "QZ", "WQ", "WZ"]
        txt = Gematria.preprocess_runes(txt, keep_tabs_breaks=True)
        lookup_keys = list(lookup.keys())
        print("shift key:", key)
        ki = 0 # key index
        for n, c in enumerate(txt):
            if c in lookup:
                shift = 0
                if key:
                    shift = key[ki % len(key)]
                if rot:
                    shift = rot
                if fast:
                    for i in range(len(results)):
                        # In Vigenere for page 3 "Welcome", plaintext F doesn't use the key and 
                        # the continuation is on the next character. Sections are marked by ':'
                        if c in overrides and n > 0 and txt[n-1] == ':':
                            shift = 0
                            ki -= 1
                        results[i] += lookup[lookup_keys[(lookup_keys.index(c) + shift) % len(lookup_keys)]][0]
                else:
                    # In Vigenere for page 3 "Welcome", plaintext F doesn't use the key and 
                    # the continuation is on the next character
                    if c in overrides and n > 0 and txt[n-1] == ':':
                        shift = 0
                        ki -= 1
                    candidates = lookup[lookup_keys[(lookup_keys.index(c) + shift) % len(lookup_keys)]]
                    stash = []
                    if len(candidates) > 1:
                        stash += stash
                    # Already figured out from list of results, explicitly set and skip O(scary)
                    if c in overrides:
                        for i in range(len(results)):
                            results[i] += overrides[c]
                        continue
                    for candidate in candidates:
                        # Shallow copy, that was a fucking annoying bug
                        working = results[:]
                        queued_deletion = []
                        for i in range(len(working)):
                            # filter impossible bigrams in the English language
                            if filter_impossible and working[i] and working[i][-1] + candidate[0] in impossible_bigrams:
                                queued_deletion.appened(i)
                                continue
                            else:
                                working[i] += candidate
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
                        if c != ":":
                            print(c)
        return results

if __name__ == "__main__":
    import sys
    with open("09.jpg.runes.txt", "r") as runes, open("09.jpg.runes-possibilities.txt", "w") as nine:
        data = runes.read()
        results = Gematria.rune_to_english(data, fast=True)
        for result in results:
            nine.write(result + "\n")
    with open("10.jpg.runes.txt", "r") as runes, open("10.jpg.runes-possibilities.txt", "w") as ten:
        data = runes.read()
        results = Gematria.rune_to_english(data, fast=True)
        for result in results:
            ten.write(result + "\n")
    with open("11.jpg.runes.txt", "r") as runes, open("11.jpg.runes-possibilities.txt", "w") as eleven:
        data = runes.read()
        results = Gematria.rune_to_english(data, fast=True)
        for result in results:
            eleven.write(result + "\n")
    with open("12.jpg.runes.txt", "r") as runes, open("12.jpg.runes-possibilities.txt", "w") as twelve:
        data = runes.read()
        results = Gematria.rune_to_english(data, fast=True)
        for result in results:
            twelve.write(result + "\n")
    

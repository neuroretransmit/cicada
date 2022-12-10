#!/usr/bin/env python3

import string
from pprint import pprint as pp

RUNE_LOOKUP = {
    'ᛠ': 'F',
    'ᛯ': 'U',
    'ᚣ': 'TH',
    'ᚫ': 'O',
    'ᚪ': 'R',
    'ᛞ': ['C', 'K'],
    'ᛟ': 'G',
    'ᛝ': 'W',
    'ᛚ': 'H',
    'ᛗ': 'N',
    'ᛖ': 'I',
    'ᛒ': 'J',
    'ᛏ': 'EO', 
    'ᛋ': 'P', 
    'ᛉ': 'X', 
    'ᛈ': ['S', 'Z'],
    'ᛇ': 'T', 
    'ᛄ': 'B', 
    'ᛁ': 'E', 
    'ᚾ': 'M', 
    'ᚻ': 'L', 
    'ᚹ': ['NG', 'ING'], 
    'ᚷ': 'OE', 
    'ᚳ': 'D', 
    'ᚱ': 'A',
    'ᚩ': 'AE',
    'ᚦ': 'Y',
    'ᚢ': ['IO', 'IA'],
    'ᚠ': 'EA',
}

class Gematria:
    @staticmethod
    def substitution(year=2013):
        print("YEAR:", year)
        s = {}
        if year == 2013:
            pp(RUNE_LOOKUP)
            return RUNE_LOOKUP
        elif year == 2014:
            lookup = {}
            for k, v in zip(reversed(RUNE_LOOKUP.keys()), RUNE_LOOKUP.values()):
                lookup[k] = v
            pp(lookup)
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
    def rune_to_english(txt, mode=2014, fast=True, overrides = {}):
        txt = Gematria.preprocess_runes(txt, keep_tabs_breaks=True)
        lookup = Gematria.substitution(year=mode)
        results = ['']
        impossible_bigrams = ["JQ", "QG", "QK", "QY", "QZ", "WQ", "WZ"]
        for c in txt:
            if c in lookup:
                # Single-letter runes
                if not isinstance(lookup[c], list):
                    for i in range(len(results)):
                        results[i] += lookup[c]
                # Multi-letter runes
                else:
                    candidates = lookup[c]
                    stash = []
                    if len(candidates) > 1:
                        stash += stash
                    # Already figured out from list of results, explicitly set and skip O(scary)
                    if c in overrides:
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
                            if c in lookup:
                                working[i] += candidate
                                break
                        for i in queued_deletion:
                            working.pop(i)
                        stash += working
                    results = stash
            else:
                for i, result in enumerate(results):
                    # Only let whitespace, punctuation and digits through - print others
                    if c in " \t\n" or c in string.punctuation or c in string.digits:
                        results[i] += c
                    else:
                        print(c)
        return results

if __name__ == "__main__":
    import sys
    with open("runes.txt", "r") as runes, open("possibilities.txt", "w") as possibilities:
        data = runes.read()
        results = Gematria.rune_to_english(data, mode=2014, fast=True, overrides={'ᛝ': 'ING'})
        for result in results:
            possibilities.write(result + "\n")

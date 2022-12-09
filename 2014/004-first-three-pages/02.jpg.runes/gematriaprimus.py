#!/usr/bin/env python3

import string

RUNE_LOOKUP = {
    'ᚠ': 'F',
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
    'ᛠ': 'F'
}

class Gematria:
    @staticmethod
    def substitution(year=2014):
        s = {}
        if year == 2014:
            return RUNE_LOOKUP
        elif year == 2013:
            lookup = {}
            keys = RUNE_LOOKUP.keys()
            for k, v in zip(keys, reversed(RUNE_LOOKUP.values())):
                lookup[k] = v
            return RUNE_LOOKUP
        else:
            raise NotImplementedError

    @staticmethod
    def preprocess_runes(txt, keep_tabs_breaks = True):
        preprocessed = txt.upper()
        if not keep_tabs_breaks:
            processed = txt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        # Repos like idkfa use the right rune, i opted for the left
        preprocessed = preprocessed.replace("ᛯ", "ᛡ")
        return preprocessed

    # TODO: Optimize out of O(scary) using tiered map lookups
    @staticmethod
    def rune_to_english(txt, mode=2014, fast=True, overrides = {}):
        Gematria.preprocess_runes(txt, keep_tabs_breaks=True)
        lookup = Gematria.substitution(year=2014)
        results = ['']
        impossible_bigrams = ["JQ", "QG", "QK", "QY", "QZ", "WQ", "WZ"]
        for c in txt:
            if c in lookup:
                if not isinstance(lookup[c], list):
                    for i in range(len(results)):
                        results[i] += lookup[c]
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
                            if working[i][-1] + candidate[0] in impossible_bigrams:
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
                    if c in " \n" or c in string.punctuation:
                        results[i] += c
                    else:
                        print(c)
        return results

if __name__ == "__main__":
    import sys
    with open("runes.txt", "r") as runes, open("possibilities.txt", "w") as possibilities:
        data = runes.read()
        results = Gematria.rune_to_english(data, mode=2014, overrides={
            'ᛞ': 'K', 
            'ᛈ': 'S',
            'ᚹ': 'ING', 
            'ᚢ': 'IA'
        })
        print("results:", len(results))
        for r in results:
            possibilities.write(r)

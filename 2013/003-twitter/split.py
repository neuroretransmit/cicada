#!/usr/bin/env python3

""" Split base64 file into its repeating pattern and base64 (only_pattern.txt, only_b64.txt) """

with open("./b64.txt") as b64:
    lines = b64.read().split("\n")
    only_b64 = []
    only_pattern = []
    i = 0
    for line in lines:
        if "-"*65 not in line:
            only_b64.append(line)
            i += 1
        else:
            i += 1
            break
    for line in lines[i:]:
        only_pattern.append(line)

with open("only_pattern.txt", "w") as pattern:
    pattern.write('\n'.join(only_pattern))
with open("only_b64.txt", "w") as pattern:
    pattern.write('\n'.join(only_b64))


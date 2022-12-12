#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as cmp, open(sys.argv[2], "w") as oob:
    data = cmp.read()
    for line in data.split("\n"):
        digit_strs = line.split()
        # Skip empty results
        if len(digit_strs) == 3:
            digit = int(digit_strs[1])
            oob.write(f"{digit:x}")


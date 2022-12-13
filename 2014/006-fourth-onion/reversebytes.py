#!/usr/bin/env python3

import sys

with open(sys.argv[1], "rb") as s1, open(sys.argv[2], "wb") as r:
    data = s1.read()
    for b in data[::-1]:
        r.write(b.to_bytes(1, 'big'))

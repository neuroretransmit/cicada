#!/usr/bin/env python3

""" Decode hex from TCP server, takes file as argument """

import binascii
import sys

with open(sys.argv[1] + ".bin", "w+b") as decoded:
    with open(sys.argv[1]) as hexcode:
        all_data = sorted(hexcode.read().split("\n"))
        for line in all_data:
            (offset, data) = line.split(":")
            offset = int(offset.strip(), 16)
            data = binascii.unhexlify(data.strip())
            decoded.seek(offset)
            decoded.write(data)
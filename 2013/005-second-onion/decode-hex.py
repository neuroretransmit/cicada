#!/usr/bin/env python3

""" Decode hex from TCP server, takes file as argument """

import binascii
import sys

with open(sys.argv[1] + ".bin", "w+b") as decoded:
    with open(sys.argv[1]) as hexcode:
        all_data = hexcode.read().split("\n")
        for line in all_data:
            data = binascii.unhexlify(line.strip())
            decoded.write(data)

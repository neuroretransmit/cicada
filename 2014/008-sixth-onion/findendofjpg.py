#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as jpg:
        end = False
        ending_byte = 0xD9
        skip_these = [0x00, 0x01, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8]
        data = jpg.read()
        for i, b in enumerate(data):
            if b == 0xFF and data[i+1] not in skip_these:
                length =int.from_bytes(data[i+1:i+2], byteorder="big", signed=True)
                if length == -2:
                    print("found skip marker")
                    continue
                elif b == 0xFF and data[i+1] == ending_byte:
                    print(i + 2)
                    break

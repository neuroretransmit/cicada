#!/usr/bin/env python3


with open("cmp.txt", "r") as cmp, open("oob.hex", "w") as oob:
    data = cmp.read()
    for line in data.split("\n"):
        digit_strs = line.split()
        print(digit_strs)
        digit = int(digit_strs[1])
        oob.write(hex(digit))


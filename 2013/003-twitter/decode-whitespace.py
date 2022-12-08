#!/usr/bin/env python3

""" Convert tabs/whitespaces to binary and decode ASCII """

import re

with open("./gematria.jpg.asc") as f:
    lines = [line for line in f.read().split("\n") if re.match("\s", line)]
    message = ""
    for line in lines:
        binary = ""
        for c in line:
            if c == " ":
                binary += "0"
            elif c == "\t":
                binary += "1"
        binary_int = int(binary, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        message += binary_array.decode() + "\n"
    print(message.strip())


#!/usr/bin/env python3

import binascii
from bs4 import BeautifulSoup

def decode_binary(line):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

with open("whitespace.html", "r") as whitespace:
    soup = BeautifulSoup(whitespace, features="html.parser")
    contents = soup.find_all("pre")
    # Will only return one content, obligatory loop
    for content in contents:
        whitespace = content.get_text()
    binary = ""
    message = ""
    for char in whitespace:
        if char == " ":
            binary += "1"
        elif char == "\t":
            binary += "0"
        elif char == "\n":
            message += decode_binary(binary) + "\n"
            binary = ""

with open("whitespace.asc", "w") as signed_message:
    signed_message.write(message)


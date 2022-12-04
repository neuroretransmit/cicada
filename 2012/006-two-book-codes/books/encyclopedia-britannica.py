#!/usr/bin/env python3

BOOK_CODE = "../../005-845145127.com/img/162667212858.jpg.asc"

with open(BOOK_CODE) as book_code:
    bc = [c for c in book_code.read().split("\n") if (":" in c and "Hash" not in c and "Version" not in c) or "the product of the first two primes" in c or "the first prime" in c]

with open("31447.txt", "r") as encyclopedia:
    contents = encyclopedia.read()
    lines = contents.split("\n")
    idx = 0
    for line in lines:
        if not line.startswith("CICADA"):
            idx += 1
        else:
            break
    message = ""
    for l in bc:
        if ":" in l:
            ref = l.split(":")
            line = idx + int(ref[0])
            col = int(ref[1]) - 1
            message += lines[line][col]
        elif "the first prime" in l:
            message += str(2)
        elif "the product of the first two primes" in l:
            message += str(2 * 3)
    print(message.lower())


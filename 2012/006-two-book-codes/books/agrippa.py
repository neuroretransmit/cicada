#!/usr/bin/env python3

BOOK_CODE = "../../005-845145127.com/img/everywhere.jpg.asc"

with open("agrippa.txt", "r") as agrippa:
    text = agrippa.read()
    # Poem starts on 6th line
    text = text.split("\n")[5:]

    with open(BOOK_CODE) as book_code:
        bc = [c for c in book_code.read().split("\n") if (":" in c and "Hash" not in c and "Version" not in c) or "the product of the first two primes" in c]
        message = ""
        for l in bc:
            if ":" in l:
                ref = l.split(":")
                line = int(ref[0]) - 1
                col = int(ref[1]) - 1
                message += text[line][col]
            elif "the product of the first two primes" in l:
                message += str(2 * 3)
        print(message)



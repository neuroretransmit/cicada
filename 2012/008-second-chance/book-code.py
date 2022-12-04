#!/usr/bin/env python3

with open("./the-marriage-of-heaven-and-hell-formatted.txt", "r") as book:
    with open ("./NHYLD.jpg.asc") as book_code:
        contents = book_code.read().split("\n")
        contents = [c for c in contents if ":" in c and "http:" not in c and "Hash:" not in c and "Version:" not in c]
        locations = [[int(i) for i in l.split(":")] for l in contents]
        formatted_book = book.read().split("\n")
        message = ""
        for location in locations:
            message += formatted_book[location[0] - 1][location[1] - 1]
        print(message)


#!/usr/bin/env python3

import re

chapters = []

def parse_chapter(file):
    with open(file) as chapter:
        return re.split("\d+\. ", chapter.read())

with open("./232.jpg.asc") as pgp:
    bc = [ line.replace("III", "2").replace("II", "1").replace("I", "0") 
          for line in pgp.read().split("\n") 
          if ":" in line and "Hash" not in line and "Version" not in line and "riddle" not in line 
          or line.strip() == "0" or line.strip() == "5"]

for chapter in ["book-of-the-law-I.txt", "book-of-the-law-II.txt", "book-of-the-law-III.txt"]:
    chapters.append([line.replace(" ", "").replace("\n", "") 
                     for line in parse_chapter(chapter) if not line == ''])

message = ""
for loc in bc:
    if ":" not in loc:
        message += loc
        print(message)
        continue
    ref = loc.split(":")
    chapter = int(ref[0])
    line = int(ref[1]) - 1
    letter = int(ref[2]) - 1
    message += chapters[chapter][line][letter]
print(f"Book code applied: {message}")
print(f"Replaced: {message.replace('-', '/')}")

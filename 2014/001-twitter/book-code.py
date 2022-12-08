#!/usr/bin/env python3

import re
from pprint import pprint as pp

with open("self-reliance.txt") as book, open("zN4h51m.jpg.asc") as code:
    dirty_paragraphs = book.read().split("\n\n")
    dirty_sentences = [re.split("(?<=[.!?])\s+",paragraph) for paragraph in dirty_paragraphs]
    # pp(dirty_sentences)
    
    paragraphs = []
    for i, paragraph in enumerate(dirty_sentences):
        tmp = ''
        sentences = []
        for sentence in paragraph:
            sentence = sentence.replace("\n", " ")
            if  " " in sentence[-2:]:
                tmp += sentence
            elif  "." in sentence[-2:] or "!" in sentence[-2:] or "?" in sentence[-2:] or "," in sentence[-2:]:
                tmp += sentence
            else:
                tmp += sentence
            sentences.append(tmp.split(" "))
            tmp = ""
        paragraphs.append(sentences)

    bookcode = code.read()
    codes = [line for line in bookcode.split("\n") 
                if re.match(r"^(\d+:){3}\d+|[.onion3]$", line) and line not in ["3301"]]
    decoded = ""
    for code in codes:
        if len(code) == 1:
            decoded += code
        else:
            (paragraph, sentence, word, char) = [int(x) - 1 for x in code.split(":")]
            # Skip exerpt for 45+
            if paragraph + 1 >= 45:
                paragraph += 1
            decoded += paragraphs[int(paragraph)][int(sentence)][int(word)][int(char)]
    print(decoded)


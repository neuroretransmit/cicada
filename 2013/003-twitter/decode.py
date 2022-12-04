#!/usr/bin/env python3

""" Decode tweets and write to binary (twitter.bin) """

import binascii

with open("twitter.bin", "w+b") as twitter:
    with open("tweets/full.txt") as posts:
        all_data = sorted(posts.read().split("\n"))
        for tweet in all_data:
            (offset, data) = tweet.split(": ")
            offset = int(offset, 16)
            data = binascii.unhexlify(data)
            twitter.seek(offset)
            twitter.write(data)


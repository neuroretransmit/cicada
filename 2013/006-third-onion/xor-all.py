#!/usr/bin/env python3

import binascii

DATASET_WITHOUT_EXT = "../002-3301/3301-contents/data/560"

with open("all.txt", "r") as d:
    dataset = None
    offset = None
    data = None
    for line in d.read().split("\n"):
        if line:
            print(line)
            (dataset, offset, data) = line.split(":")
            with open(f"{DATASET_WITHOUT_EXT}.{dataset}", "rb") as ds:
                data_contents = bytes.fromhex(data)
                ds.seek(int(offset))
                dataset_contents = ds.read()
                message = ''.join([chr(a^b) for a, b in zip(data_contents, dataset_contents)])
                print(message)

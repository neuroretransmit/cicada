#!/usr/bin/env python3

import binascii

with open("data.txt", "r") as data, open("../002-3301/3301-contents/data/560.13", "rb") as dataset:
    data_contents = bytes.fromhex(data.read())
    dataset.seek(12821)
    dataset_contents = dataset.read()
    message = ''.join([chr(a^b) for a, b in zip(data_contents, dataset_contents)])
    print(message)

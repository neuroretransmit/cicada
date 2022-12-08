#!/usr/bin/env python3

with open("VHRH.bin", "rb") as f, open("inverted.bin", "wb") as inverted:
    for b in f.read():
        inverted.write((b ^ 0b11111111).to_bytes(1, 'big'))


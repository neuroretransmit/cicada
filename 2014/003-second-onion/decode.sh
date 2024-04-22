#!/bin/sh

# Convert hex (512 char)
xxd -r -p 512.txt > 512.bin
# Convert hex (large)
tail -n +2 VHRH.txt | xxd -r -p > VHRH.bin
# Flip all bits
./flipbits.py

# Extract using found offsets of SOI/EOI in JPG file format
dd if=inverted.bin of=00.jpg bs=1 skip=0 count=168876
dd if=inverted.bin of=01.jpg bs=1 skip=168876 count=1476614
dd if=inverted.bin of=02.bin bs=1 skip=1645490 count=175159
< 02.bin xxd -p -c1 | tac | xxd -p -r > 02.jpg

# Run outguess
outguess -r 00.jpg 00.jpg.asc
outguess -r 01.jpg 01.jpg.asc
outguess -r 02.jpg 02.jpg.asc


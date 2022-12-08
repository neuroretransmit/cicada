#!/bin/sh

# Convert hex (512 char)
xxd -r -p 512.txt > VHRH.bin
# Convert hex (large)
tail -n +2 VHRH.txt | xxd -r -p > VHRH.bin
# Flip all bits
./flipbits.py

# Detect/extract packed files with binwalk, not including stegdetect results.
# binwalk --dd='.*' inverted.bin
# mv _inverted.jpg.extracted/293AC intermediate.jpg
# rm -rf _inverted.jpg.extracted

# Extract using found offsets of SOI/EOI in JPG file format
dd if=inverted.bin of=00.jpg bs=1 skip=0 count=168876
dd if=inverted.bin of=02.jpg bs=1 skip=168876 count=1476614
dd if=inverted.bin of=01.bin bs=1 skip=1645490 count=175159
< 01.bin xxd -p -c1 | tac | xxd -p -r > 01.jpg

# Run outguess
outguess -r 00.jpg 00.jpg.asc
outguess -r 01.jpg 01.jpg.asc
outguess -r 02.jpg 02.jpg.asc


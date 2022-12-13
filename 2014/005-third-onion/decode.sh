#!/bin/sh

# convert <!--3301--> hex to data
xxd -r -p onion3.hex > onion3.bin
# reverse bytes for the reversed image on the end
./reversebytes.py onion3.bin onion3-reversed.bin
# generate comparison of byte values and save it
cmp -l onion3.bin onion3-reversed.bin > onion3-cmp.txt
# Extract ONLY the first image - no extra garbage
dd if=onion3.bin bs=1 count=$(./findendofjpg.py onion3.bin) status=noxfer > 03.jpg
# get outguess message
outguess -r 03.jpg 03.jpg.asc
# decrypt message, remove not from Cicada for hex, and convert to binary for hint image
gpg -d 03.jpg.asc | tail -n +6 | xxd -r -p > 03.jpg.asc.jpg

# convert server status hex to data
xxd -r -p server-status.hex > server-status.bin
# reverse byte for reversed/appended image
./reversebytes.py server-status.bin server-status-reversed.bin
# compare files byte-by-byte
cmp -l server-status.bin server-status-reversed.bin > server-status-cmp.txt
# extract the magic square
dd if=server-status.bin bs=1 skip=$((0x00521e4)) count=357 status=noxfer | rev | xxd -p -r > square.txt
# Extract ONLY the first image - no extra garbage
dd if=server-status.bin bs=1 count=$(./findendofjpg.py server-status.bin) status=noxfer > 04.jpg
./gematriaprimus.py
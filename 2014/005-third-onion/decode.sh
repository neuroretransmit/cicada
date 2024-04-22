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

# use infotomb server status to extract next two pages
xxd -r -p infotomb-server-status.hex > infotomb-server-status.bin
# reverse
./reversebytes.py infotomb-server-status.bin infotomb-server-status-reversed.bin
# compare reversed/forward
cmp -l infotomb-server-status.bin infotomb-server-status-reversed.bin
# extract page 4
dd if=infotomb-server-status-reversed.bin bs=1 count=$(./findendofjpg.py infotomb-server-status-reversed.bin) status=noxfer > 04.jpg
outguess -r 04.jpg 04.jpg.bin

# convert server status hex to data
xxd -r -p server-status.hex > server-status.bin
# Extract ONLY the first image - page 5 - no extra garbage
dd if=server-status.bin bs=1 count=$(./findendofjpg.py server-status.bin) status=noxfer > 05.jpg
# extract magic square text file
dd if=server-status.bin bs=1 skip=$((0x00521e4)) count=357 status=noxfer | rev | xxd -p -r > square.txt
./gematriaprimus.py

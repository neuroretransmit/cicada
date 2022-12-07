#!/bin/sh

# Solve for the PGP message in XOR
gpg -d ../003-second-onion/00.jpg.asc > 00.asc.hex
gpg -d ../003-second-onion/01.jpg.asc > 01.asc.hex
gpg -d ../003-second-onion/02.jpg.asc > 02.asc.hex
xxd -r p 00.asc.hex > 00.asc.bin
xxd -r p 01.asc.hex > 01.asc.bin
xxd -r p 02.asc.hex > 02.asc.bin
./xor.py 00.asc.bin 01.asc.bin 00^01.bin
./xor.py 00^01.bin 02.asc.bin 00^01^02.asc
gpg --verify 00^01^02.asc
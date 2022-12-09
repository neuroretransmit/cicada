#!/bin/sh

xxd -r -p server-status.hex -> server-status.jpg
./reversebytes.py
cmp -l server-status.jpg ./server-status-reversed.jpg > cmp.txt
# Extract magic square
dd if=server-status.jpg bs=1 skip=$((0x00521e4)) count=357 status=noxfer | rev | xxd -p -r > square.txt


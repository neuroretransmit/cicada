#!/bin/sh

xxd -r -p avowyfg151kzfj3n_update_after_downtime.html > decoded.gz
gunzip -k decoded.gz
dd if=decoded bs=1 count=$(./findendofjpg.py decoded) status=noxfer > 06.jpg
dd if=decoded bs=1 skip=$(./findendofjpg.py decoded) status=noxfer > 06-trimmed.bin
dd if=06-trimmed.bin bs=1 count=$(./findendofjpg.py 06-trimmed.bin) > 07.jpg
dd if=06-trimmed.bin bs=1 skip=$(./findendofjpg.py 06-trimmed.bin) status=noxfer > "06,07-trimmed.bin"
./reversebytes.py "06,07-trimmed.bin" "06,07-trimmed-reversed.bin"
dd if="06,07-trimmed-reversed.bin" bs=1 count=$(./findendofjpg.py "06,07-trimmed-reversed.bin") status=noxfer > 08.jpg
outguess -r 08.jpg 08.jpg.asc
dd if="06,07-trimmed-reversed.bin" bs=1 skip=$(./findendofjpg.py "06,07-trimmed-reversed.bin") status=noxfer > "06,07,08-trimmed.bin"
dd if="06,07,08-trimmed.bin" bs=1 count=$(./findendofjpg.py "06,07,08-trimmed.bin") > 09.jpg
./gematriaprimus.py

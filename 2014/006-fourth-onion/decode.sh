#!/bin/sh

xxd -r -p avowyfg151kzfj3n_update_after_downtime.html > decoded.gz
gunzip -k decoded.gz
dd if=decoded bs=1 count=$(./findendofjpg.py decoded) status=noxfer > 05.jpg
dd if=decoded bs=1 skip=$(./findendofjpg.py decoded) status=noxfer > 05-trimmed.bin
dd if=05-trimmed.bin bs=1 count=$(./findendofjpg.py 05-trimmed.bin) > 06.jpg
dd if=05-trimmed.bin bs=1 skip=$(./findendofjpg.py 05-trimmed.bin) status=noxfer > "05,06-trimmed.bin"
./reversebytes.py "05,06-trimmed.bin" "05,06-trimmed-reversed.bin"
dd if="05,06-trimmed-reversed.bin" bs=1 count=$(./findendofjpg.py "05,06-trimmed-reversed.bin") status=noxfer > 07.jpg
dd if="05,06-trimmed-reversed.bin" bs=1 skip=$(./findendofjpg.py "05,06-trimmed-reversed.bin") status=noxfer > "05,06,07-trimmed.bin"
dd if="05,06,07-trimmed.bin" bs=1 count=$(./findendofjpg.py "05,06,07-trimmed.bin") > 08.jpg
./gematriaprimus.py

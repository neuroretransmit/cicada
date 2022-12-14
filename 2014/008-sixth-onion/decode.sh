#!/bin/sh

xxd -r -p ./ut3qtzbrvs7dtvzp.hex > ./ut3qtzbrvs7dtvzp.bin
dd if=./ut3qtzbrvs7dtvzp.bin bs=1 count=$(./findendofjpg.py ./ut3qtzbrvs7dtvzp.bin) status=noxfer > 09.jpg
dd if=./ut3qtzbrvs7dtvzp.bin bs=1 skip=$(./findendofjpg.py ./ut3qtzbrvs7dtvzp.bin) status=noxfer > 09-trimmed.bin
dd if="09-trimmed.bin" bs=1 count=$(./findendofjpg.py 09-trimmed.bin) > 10.jpg
dd if="09-trimmed.bin" bs=1 skip=$(./findendofjpg.py 09-trimmed.bin) status=noxfer > "09,10-trimmed.bin"
dd if="09,10-trimmed.bin" bs=1 count=$(./findendofjpg.py "09,10-trimmed.bin") > 11.jpg
dd if="09,10-trimmed.bin" bs=1 skip=$(./findendofjpg.py "09,10-trimmed.bin") status=noxfer > "09,10,11-trimmed.bin"
dd if="09,10,11-trimmed.bin" bs=1 count=$(./findendofjpg.py "09,10,11-trimmed.bin") > 12.jpg
./gematriaprimus.py

for f in $(ls *.jpg); do
	outguess -r $f $f.asc
done

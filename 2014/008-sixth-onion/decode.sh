#!/bin/sh

xxd -r -p ./ut3qtzbrvs7dtvzp.hex > ./ut3qtzbrvs7dtvzp.bin
dd if=./ut3qtzbrvs7dtvzp.bin bs=1 count=$(./findendofjpg.py ./ut3qtzbrvs7dtvzp.bin) status=noxfer > 10.jpg
dd if=./ut3qtzbrvs7dtvzp.bin bs=1 skip=$(./findendofjpg.py ./ut3qtzbrvs7dtvzp.bin) status=noxfer > 10-trimmed.bin
dd if="10-trimmed.bin" bs=1 count=$(./findendofjpg.py 10-trimmed.bin) > 11.jpg
dd if="10-trimmed.bin" bs=1 skip=$(./findendofjpg.py 10-trimmed.bin) status=noxfer > "10,11-trimmed.bin"
dd if="10,11-trimmed.bin" bs=1 count=$(./findendofjpg.py "10,11-trimmed.bin") > 12.jpg
dd if="10,11-trimmed.bin" bs=1 skip=$(./findendofjpg.py "10,11-trimmed.bin") status=noxfer > "10,11,12-trimmed.bin"
dd if="10,11,12-trimmed.bin" bs=1 count=$(./findendofjpg.py "10,11,12-trimmed.bin") > 13.jpg
./gematriaprimus.py

for f in $(ls {10,11,12,13}.jpg); do
	outguess -r $f $f.asc
done

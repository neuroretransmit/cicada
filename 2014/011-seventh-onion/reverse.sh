#!/bin/sh

for f in $(ls *.jpg); do
	./reversebytes.py $f $f-reversed.bin
	file $f-reversed.bin
	binwalk $f-reversed.bin
done

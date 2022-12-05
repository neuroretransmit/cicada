#!/bin/sh

./decode-hex.py ./icmp-echo.txt
mv icmp-echo.txt.bin icmp-echo.asc.gz
gunzip -c ./icmp-echo.asc.gz > icmp-echo.asc

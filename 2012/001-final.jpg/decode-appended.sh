#!/bin/sh

cat appended.txt | sed 's/.*\"\(lxxt.*\)\"/\1/g' | perl -pne 'chomp;s{(.)}{chr(ord($1)-4)}sgex;$_.=chr(10)'

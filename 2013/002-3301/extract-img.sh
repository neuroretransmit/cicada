#!/bin/sh

mv 3301.img 3301-decompressed.img.gz
gunzip 3301-decompressed.img.gz
binwalk -eM 3301-decompressed.img

#!/bin/sh

gpg -d ./q4utgdi2n4m4uim5.asc > ./q4utgdi2n4m4uim5.asc.hex
xxd -r -p ./q4utgdi2n4m4uim5.html.hex > ./interconnectedness.mp3
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./logicgates.py
deactivate
cp ./q4utgdi2n4m4uim5.onion.jpeg ./q4utgdi2n4m4uim5.onion.jpg
outguess -r ./q4utgdi2n4m4uim5.onion.jpg ./q4utgdi2n4m4uim5.onion.asc.bz2
rm ./q4utgdi2n4m4uim5.onion.jpg
bzip2 -f -k -d ./q4utgdi2n4m4uim5.onion.asc.bz2
xxd -r -p 01.hex > 01.jpg
xxd -r -p 02.hex > 02.jpg
xxd -r -p 03.hex > 03.mp3


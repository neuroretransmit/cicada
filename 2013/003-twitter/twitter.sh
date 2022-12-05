#!/bin/sh

CONTENTS="../002-3301/3301-contents"

./png.sh
./xor.py "$CONTENTS/data/560.13" "decoded.png" "560.13^decoded.png.bin"
./xor.py "560.13^decoded.png.bin" "$CONTENTS/audio/761.mp3" "560.13^b64.txt.bin"
./xor.py "./twitter.bin" "$CONTENTS/audio/761.mp3" "gematria.jpg"
outguess -r "gematria.jpg" "gematria.jpg.asc"
cat "gematria.jpg.asc"
./decode-whitespace.py > whitespace-message.txt
cat whitespace-message.txt
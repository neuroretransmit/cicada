#!/bin/sh

# XOR two pictures together
# $1 and $2 are the two images to combine
# $3 is the output image
xorpics() {
        if [ $# -ne 3 ]; then
                echo "USAGE: xorpics <pic1> <pic2> <outfile>"
                return 1
        else
                convert $1 $2 -fx "(((255*u)&(255*(1-v)))^((255*(1-u))&(255*v)))/255" $3
        fi
}

gpg -d ./q4utgdi2n4m4uim5.html > ./q4utgdi2n4m4uim5.html.hex
xxd -r -p ./q4utgdi2n4m4uim5.html.hex > ./q4utgdi2n4m4uim5.html.mp3
xorpics ./q4utgdi2n4m4uim5.onion.jpeg Francisco_de_Goya_y_Lucientes_-_Portrait_of_Andrés_del_Peral_-_WGA10031.jpg xor.jpg
cp ./q4utgdi2n4m4uim5.onion.jpeg ./q4utgdi2n4m4uim5.onion.jpg
outguess -r ./q4utgdi2n4m4uim5.onion.jpg ./q4utgdi2n4m4uim5.onion.asc.bz2
bzip2 -f -k -d ./q4utgdi2n4m4uim5.onion.asc.bz2
gpg -d ./q4utgdi2n4m4uim5.onion.asc > q4utgdi2n4m4uim5.onion.hex
xxd -r -p ./q4utgdi2n4m4uim5.onion.hex > q4utgdi2n4m4uim5.onion.bin

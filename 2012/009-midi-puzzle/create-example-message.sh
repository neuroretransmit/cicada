#!/bin/sh

GPG="gpg --no-default-keyring --keyring=$(pwd)/example-keyring.gpg"

$GPG --fingerprint
$GPG --recv-keys "6D854CD7933322A601C3286D181F01E57A35090F"
$GPG -e --armor -r "Cicada 3301 (845145127)" -r "solver@cicada-solver" words.txt
$GPG --clearsign words.txt.asc
$GPG --verify words.txt.asc.asc
$GPG -d words.txt.asc.asc > decrypted.asc
$GPG -d decrypted.asc

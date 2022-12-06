#!/bin/sh

PORT=${PORT:-3301}

server="nc -C localhost ${PORT} -N"
tests=("quine" "code" "koan" "rand" "base29" "next1" "next2" "goodbye" "dh1" "dh2" "goodbye")
for t in "${tests[@]}"; do
 cat $t | $server
done

#!/bin/bash
input="./wordlist.txt"
while IFS= read -r line; do
    for f in $(ls *.jpg); do
        outguess -k"$line" -r $f $f.outguess
        file_results="$(file $f.outguess)"
        if [[ $file_results != *"data" && $file_results != *"empty" && $file_results != "exception" ]]; then
            echo $file_results
            read -p "Press Enter to continue" </dev/tty
        fi
    done
done < "$input"


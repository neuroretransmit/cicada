#!/usr/bin/env bash

while read p; do
  echo $p
  unrar x trailing.rar -p"$p"
  if [[ $? -ne 3 ]]; then
    break
  fi
done < "Parsed Wordlists 2024-04-21-12-19-10/^^MASTER_WORDLIST-2024-04-21-12-19-10.txt"


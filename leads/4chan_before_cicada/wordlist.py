#!/usr/bin/env python3
## THIS SCRIPT REQUIRES PYTHON 3.7.x OR ABOVE

## Wordlist generation using text files as sources of words
## Author: JG
## Date: Nov 2018

## This script will parse any text files that it finds in the present directory
## and any subdirectories of that directory, and will create a wordlist from those
## text files of all of the unique words it finds inside the files in alphabetical order.
## The wordlists will be saved with the original filename, with the phrase
## '-sorted-wordlist' appended to it, in a folder called 'Parsed Wordlists'

## The script will then combine all of the wordlists into a 'master wordlist'
## which is again sorted alphabetically.

import glob  # FOR FOLDER PARSING
import os  # FOR FILE HANDLING
import string  # FOR REMOVING UNWANTED CHARS
from datetime import datetime  # FOR ADDING TIMESTAMP TO FILENAME

# SPECIFY START POINT FOR SEARCH ('.' IS CURRENT LOCATION OF THIS SCRIPT)

rootdir = '.'

# SET DATE STRING

datestring = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')

# MAKE 'WORDLISTS FOLDER' IN CURRENT LOCATION TO STORE WORDLISTS

wordlists_folder = "Parsed Wordlists " + datestring
os.mkdir(wordlists_folder)

# SET TYPE OF FILES TO SEARCH THROUGH

file_extensions = ('.txt', '.rtf')

# DEFINE MASTER WORDLIST

master_wordlist = []

# DEFINE SEARCH METHOD FOR WORDS IN FILES

def get_words(file_object):
    for line in file_object:
        line = line.strip().translate(str.maketrans('','', string.punctuation + string.digits))
        for word in line.split():
            word = word.lower()
            yield word

# PARSE THROUGH FILES IN CURRENT DIR AND SUBDIRS

for extensions in file_extensions:
    for inputfile in glob.glob(os.path.join(rootdir, '**/*' + extensions), recursive=True):
        with open(inputfile, 'r', encoding="utf-8") as infile:

            unique_words = sorted(set(get_words(infile)))

            outfile = os.path.join(wordlists_folder, os.path.basename(os.path.splitext(inputfile)[0]) + "-sorted-wordlist.txt")

            with open(outfile,'w', encoding="utf-8") as f:
                for item in unique_words:
                    f.write("%s\n" % item)

                    if item not in master_wordlist:
                        master_wordlist.append(item)

            print("Name of output wordlist: " + outfile)
            print("Length of wordlist = ", len(unique_words))

# CREATE MASTER WORDLIST THAT COMBINES ALL

with open(os.path.join(wordlists_folder, "^^MASTER_WORDLIST-" + datestring + ".txt"),'w', encoding="utf-8") as f:
    unique_master = sorted(set(master_wordlist))
    for item in unique_master:
        f.write("%s\n" % item)

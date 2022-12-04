#!/usr/bin/env python3
"""
Context: Using the Maya numerals from the banner of the subreddit,
it was deduced that a was 10 and other letters followed suit from
this starting point with their position in the alphabet. This 
decodes the remaining letters in the subreddit's info for the
Vigenere key.
"""

SUBREDDIT_INFO = "a2e7j6ic78h0j7eiejd0120"

key = []

def reversal(sub_str):
    """ Reverse non-digits to their digit counterparts; subtract ASCII value of 'a' and subtract 10 from that """
    for c in sub_str:
        if c.isdigit():
            key.append(int(c))
        else:
            key.append(ord(c) - (ord('a') - 10))

if __name__ == "__main__":
    reversal(SUBREDDIT_INFO)
    print(key)


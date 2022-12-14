#!/usr/bin/python3

import itertools

def decrypt(key, ciphertext):
	print("key:", key)
	decrypt = ""
	for line in ciphertext.split("\n"):
		for i in range(len(line)):
			k = key[i]
			decrypt += line[k]
		decrypt += "\n"
	print(decrypt.replace("\n", ""))

ciphertext = """TLBEIEO
VUTHTRE
IDTSEOS
TPOSOYR
SLBTIII
YT4DGUQ
IMNU442
I15339M"""
# for key in itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]):
	# decrypt(key, ciphertext)
decrypt([0,6,2,5,1,4,3], ciphertext)

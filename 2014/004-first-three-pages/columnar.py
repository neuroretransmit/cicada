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
	print(decrypt)

ciphertext = """IDGTKUMLOOARWO
ERTHISUTETLHUT
IATSLLOUIMNITE
LNJ7TFYVOIUAUS
NOCO5JI4MEODZZ"""
# for key in itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]):
	# decrypt(key, ciphertext)
decrypt([2, 8, 9, 1, 12, 13, 11, 4, 5, 7, 3, 0, 6, 10], ciphertext)

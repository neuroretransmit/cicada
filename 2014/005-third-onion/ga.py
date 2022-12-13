#!/usr/bin/env python3

import random
import string
from gematriaprimus import Gematria

DIST = 0
KEY = 1
DECRYPT = 2
TARGET = "AUOWYFG151KZFJ3NONIAN"
valid_chromosomes = string.ascii_uppercase
DOUBLES = True

def levenshtein_distance(x, y):
    n = len(x)
    m = len(y)

    A = [[i + j for j in range(m + 1)] for i in range(n + 1)]

    for i in range(n):
        for j in range(m):
            A[i + 1][j + 1] = min(A[i][j + 1] + 1,              # insert
                                  A[i + 1][j] + 1,              # delete
                                  A[i][j] + int(x[i] != y[j]))  # replace
    return A[n][m]

class GA:
    """ Individuals in pool should be (lev_dist, key, decrypt) """
    def __init__(self, p1, p2):
        self.pool = [p1, p2]

    # Fitness should involve dna split lengths as well to find the best segment to mutate
    def evolve(self):
        while True:
            # rank fitness
            self.pool.sort(key=lambda e: e[DIST])
            # select two fittest
            parents = self.pool[0:2]
            print("BEST:", parents[0], parents[1])
            if parents[0][DIST] == 0:
                break
            # crossover DNA
            split = random.randint(0, len(parents[0][KEY]))
            offspring_key = parents[0][KEY][:split] + parents[1][KEY][split:]
            # mutate (limit to last 5 characters since we know it is WELHOMEPILGRIM)
            key_split = random.randint(0, len(offspring_key))
            size = random.randint(-5, 5)
            offspring_key = (offspring_key[:key_split + size] + random.choice(valid_chromosomes) + offspring_key[key_split:size])[:len(TARGET) + size]
            # create data for ranking
            offspring_decrypts = Gematria.rune_to_english(data, mode="vigenere", key=Gematria.key_to_shifts(offspring_key, doubles=DOUBLES), fast=False, filter_impossible=False)
            offspring_dists = []
            for d in offspring_decrypts:
                offspring_dists.append(levenshtein_distance(d, TARGET))
            # during evolution, pick distance of best permutation
            offspring_dist = min(offspring_dists)
            offspring_decrypt = [offspring_decrypts[i] for i, d in enumerate(offspring_dists) if d == offspring_dist][0]
            # create offspring and add to pool
            offspring = (offspring_dist, offspring_key, offspring_decrypt)
            if offspring not in self.pool:
                self.pool.append(offspring)


if __name__ == "__main__":
    with open("./03.jpg.asc.jpg.runes.txt", "r") as runes:
        data = runes.read()
        p1_key = 'WELHOMEPILGRIMTOTHEEND'
        p1_dists = []
        p1_decrypts = Gematria.rune_to_english(data, mode="vigenere", key=Gematria.key_to_shifts(p1_key, doubles=DOUBLES), fast=False, filter_impossible=False)
        for d in p1_decrypts:
            p1_dists.append(levenshtein_distance(d, TARGET))
        p1_dist = min(p1_dists)
        p1_decrypt = [p1_decrypts[i] for i, d in enumerate(p1_dists) if d == p1_dist][0]
        p1 = (p1_dist, p1_key, p1_decrypt)
        p2_key = 'WELCOMEPILGRIMTOTHEEND'
        p2_dists = []
        p2_decrypts = Gematria.rune_to_english(data, mode="vigenere", key=Gematria.key_to_shifts(p2_key, doubles=DOUBLES), fast=False, filter_impossible=False)
        for d in p2_decrypts:
            p2_dists.append(levenshtein_distance(d, TARGET))
        p2_dist = min(p2_dists)
        p2_decrypt = [p2_decrypts[i] for i, d in enumerate(p2_dists) if d == p2_dist][0]
        p2 = (p2_dist, p2_key, p2_decrypt)
        ga = GA(p1, p2)
        ga.evolve()
        
        


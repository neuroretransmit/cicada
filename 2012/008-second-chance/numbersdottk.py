#!/usr/bin/env python3

import random

def primesbelow(N):
    correction = N % 6 > 1
    N = {0:N, 1:N-1, 2:N+4, 3:N+3, 4:N+2, 5:N+1}[N%6]
    sieve = [True] * (N // 3)
    sieve[0] = False
    for i in range(int(N ** .5) // 3 + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k*k // 3::2*k] = [False] * ((N//6 - (k*k)//6 - 1)//k + 1)
            sieve[(k*k + 4*k - 2*k*(i%2)) // 3::2*k] = [False] * ((N // 6 - (k*k + 4*k - 2*k*(i%2))//6 - 1) // k + 1)
    return [2, 3] + [(3 * i + 1) | 1 for i in range(1, N//3 - correction) if sieve[i]]

smallprimeset = set(primesbelow(100000))
smallprimes = (2,) + tuple(n for n in range(3,1000,2) if n in smallprimeset)
_smallprimeset = 100000
def isprime(n, precision=7):
    if n < 1:
        raise ValueError("Out of bounds, first argument must be > 0")
    elif n <= 3:
        return n >= 2
    elif n % 2 == 0:
        return False
    elif n < _smallprimeset:
        return n in smallprimeset


    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for repeat in range(precision):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
    
        if x == 1 or x == n - 1: continue
    
        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == 1: return False
            if x == n - 1: break
        else: return False

    return True

def pollard_brent(n):
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g==1:
            ys = y
            for i in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x-y) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break
    return g

def bigfactors(n, sort = False):
    factors = []
    while n > 1:
        if isprime(n):
            factors.append(n)
            break
        factor = pollard_brent(n) 
        factors.extend(bigfactors(factor,sort))
        n //= factor

    if sort: factors.sort()    
    return factors

def primefactors(n, sort=False):
    factors = []

    limit = int(n ** .5) + 1
    for checker in smallprimes:
        if checker > limit: break
        while n % checker == 0:
            factors.append(checker)
            n //= checker


    if n < 2: return factors
    else : 
        factors.extend(bigfactors(n,sort))
        return factors

agrippa = sorted([
    644169769482,
    876873892385,
    935691396441,
    963846244281
])

britannica = sorted([
    162667212858,
    414974253863,
    598852142735,
    316744223127,
    427566844663,
    889296759263,
])

numbers = max(agrippa) + max(britannica)
print(f"\"Numbers dot TK\" => {numbers}.tk")
print(f"\"Go to my largest part\" => {max(primefactors(numbers))}.tk")



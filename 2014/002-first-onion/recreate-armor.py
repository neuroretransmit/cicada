#!/usr/bin/env python3

from Crypto.PublicKey import RSA

n = int("10412790658919985359827898739594318956404425106955675643739226952372682423852959081739834390370374475764863415203423499357108713631", 10);
d = int("8405289400463632230734020463585740290701541068528757082336582147849608437487044193183300124532157613486661010511755054111493372145", 10);
e = int("65537", 10);

privateKey = RSA.construct((n, e, d))
privateKeyPem = privateKey.exportKey() # export in PKCS#8 format

publicKey = RSA.construct((n, e))
publicKeyPem = publicKey.exportKey() # export in X.509/SPKI format

print(privateKeyPem.decode('utf8'))
print(publicKeyPem.decode('utf8'))

# Hidden service reply

On May 2nd, 2014 3301 distributes messages to the hidden services that submitted magic squares. The requests looked like the following, note the user-agent string.

```
127.0.0.1 - - [02/May/2014:10:**:** +0200] "GET /key.asc HTTP/1.1" 200 * "-" "Cicada/33.01 CicaDOS 1.033 E Edition"PP
127.0.0.1 - - [02/May/2014:10:**:** +0200] "GET / HTTP/1.1" 200 * "-" "Cicada/33.01 CicaDOS 1.033 E Edition"
127.0.0.1 - - [02/May/2014:11:**:** +0200] "POST /cgi-bin/upload HTTP/1.1" 200 * "-" "Cicada/33.01 Cic/DOS/ 1.033 S Edition"
```

## message.txt.asc

See [message.txt.asc](message.txt.asc). This gave the path to the next onion. 

### Whitespace

It is another signed message containg unneccessary whitespace.

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1
 ]1
Hello.  Your enlightenment awaits you.  ]2
   ]3
     ]5ky2khlqdf7qdznac.onion      ]6
           ]11
We look forward to hearing from you.
             ]13
                 ]17
Good luck.                      ]22
                             ]29
3301
                               ]31
                                     ]37
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)
 
iQIcBAEBAgAGBQJTO88vAAoJEBgfAeV6NQkPEfsQAI0jGcmBaQr2AGGr1/ic839I
fc58EyVNLgWs6Aox0/Dc2Tj8dXOxc0sBNWY98tICIy2T0Vbpf1VF65nFs+cVcxXI
pXIU5X0O3XKRfxequIZQQUnt4elLIfFAIgrXbE9N7K5qkD47xg4kaYkPQh7/mDBa
NBVHsLkw8bbLUo7lBtv5VFHTeTikSnT3m7FsoSHl5WlsY9WvITO5VcYd48jFbBSS
P9Uk7v7cg1ohWpDB0BiYUTfOVxXYuZpnFiR6vAADP5KkY/qrFF7wrpYbhSmageId
Qcxyc/dajUTlwK7dl+OwAJn4XRPceBPMjW9SbCr33y1C3ijCuxn06penu0KnUyge
yYjyedXg11UPb/B6eT+hwAOPg/DLDTQ57QOQlGOX19lB56iZbHKuglQZUZ5kJq54
dTobWhi6FBtwu+QLnJCz2SASLCuKDIWFkwSoYro/F9Zlo7b0UUO2IOkcKw7tKzq9
uyPtBDQayCSIIHJhVjAtNiVFjNe+TcBf1VppAGY/7jfUfwxJ7Sfbv5Jwll+6MDYr
YdsnJBZjhLuoxFyr9g4TF0OTXmxT+TyAZ4qoItu4C0bcEncBcfLJz+J74X1upsZl
DMq7On1paQAkXvzr6ywDBpMJbDZETkl9gZbzHn1Ji+9f3fANrqU+5kZ1su2OReQf
++CO13gAUF4WohKip4mC
=VAo/
-----END PGP SIGNATURE-----
```
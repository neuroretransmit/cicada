# Valēte!

After a month of no communication from Cicada, another image was posted in [r/a2e7j6ic78h0j](../003-subreddit/README.md).

On February 6, 2012 11:27:05 PM the following image was posted to the subreddit by user CageThrottleUs which signaled an end of the puzzle. It is important to note - the moderator badge is now gone. 

![vjuNp.jpg](../003-subreddit/posts/vjuNp.jpg)

## Outguess

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Hello.
  
We have now found the individuals we sought.   
Thus our month-long journey ends.     
       
For now.           
             
Thank you for your dedication and effort.  If you 
were unable to complete the test, or did not receive 
an email, do not despair.  
           
There will be more opportunities like this one.
       
Thank you all.
     
3301
   
  
P.S. 1041279065891998535982789873959431895640\
442510695567564373922695237268242385295908173\
9834390370374475764863415203423499357108713631

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJPMFtcAAoJEBgfAeV6NQkPiyIQAMBkZSKkzNqkRiiw4OeEDiRE
eMOHNOOpy+r4+p898RmS4+QlrpyDjyRxeto5RVYqYuzqgZHBMF9EMSfSLqE3PKIG
Jta4mIggG1Xte+zwVzXBdVBk/4vWqqdMPBtZ4kQjfoc2n3/pUK+eGqmtxWLIzyUL
iug0zmWFN1ZOOMfXcWOfXsiRD9neSxxLwGDY91vxJSTUH7yfC21Mot2eom1PAki8
cwJqt2H56hUmJ339edHcXqLnUxvIbEa/so6hgSrA3U/A0EiTjzJ2YWuPqc4N866D
a9tgz0euQsZtl0XqtJZ48DWPja3bLDJYeRed1Qr+bAdXEgPBNgJQgT8kjcAhdqj/
TPvoYTXMQwvbT5IDiuYum4Vn2h4Z7BX8l7VdZBLNdgjapNohgOy+00DJFp8bG7em
mPlheAl7aLyHzbKPrpINCdgJhe4KfhPDhdsWFYJA99S61wwHPKlOrCgLGEcvH1YC
pOZKFZfCO+BMu2rz3JCfrSuGvyDwq54F8/Jc5zlHYCGNcTsvU0JO8F/ykNetl1qY
AIDNR9VHVwdR9/XiVTGXj0iOUKp1pzJlUY1Zi95vxNMC/WpiUu/AepEOLVIy/nsz
iAU8Xhke5xJPjKHb6pJOgH8gfe0QjuRacvg2oJL2YAKR/MT95kJmW7Wl+m68fcED
Cvvt7a3uW/YLSOL/S4/6
=HMPw
-----END PGP SIGNATURE-----
```

## Unused

There are two unused clues from this image.

### Whitespace

There is appended whitespace to this outguess message. My attempts to get a message out with `snow` (whitespace steganography tool) have proved to be futile. Other ideas may be book code locations, etc.

```
Hello.]0
  ]2
We have now found the individuals we sought.   ]3
Thus our month-long journey ends.     ]5
       ]7
For now.           ]11
             ]13
Thank you for your dedication and effort.  If you ]1
were unable to complete the test, or did not receive ]1
an email, do not despair.  ]2
           ]11
There will be more opportunities like this one.]0
       ]7
Thank you all.]0
     ]5
3301]0
   ]3
  ]2
P.S. 1041279065891998535982789873959431895640\]0
442510695567564373922695237268242385295908173\]0
9834390370374475764863415203423499357108713631]0
```

### Number

The number was also never used, following programming language/shell line continuations - this is likely just one full number.

`10412790658919985359827898739594318956404425106955675643739226952372682423852959081739834390370374475764863415203423499357108713631`

It factors into `99554414790940424414351515490472769096534141749790794321708050837` and `104593961812606247801193807142122161186583731774511103180935025763`.

See [factor.sh](../008-rsa-emails/factor.sh) for verification, prepare to wait a long time.

I've recreated a public/private key in the event this is another RSA key for later use. See [recreate-pk.pl](recreate-pk.pl), [numbers.private](numbers.private) (perl), [numbers.public](numbers.public) (perl), and [recreated.key](recreated.key) (armored version, created with [recreate-armor.py](recreate-armor.py)). There is also [attempt-pgp-recreation.sh](attempt-gpg-recreation.sh) using a tool called monkeysphere to import the RSA key to a PGP key, again failed.

```bash
$ ./monkeysphere/src/pem2openpgp "it worked" < recreated.pem | gpg2 --import --homedir temp_gpg/
RSA.xs:713: OpenSSL error: digest too big for rsa key at ./monkeysphere/src/pem2openpgp line 633, <STDIN> line 1.
gpg: no valid OpenPGP data found.
gpg: Total number processed: 0
```

This has been used for numerous trolls, notably "the game" decrypt found in an ideone page. 

What if Cicada wanted to increase the signal to noise ratio in its absence and pass along the tools to do it? :thinking-face:

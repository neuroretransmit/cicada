# auqgnxjtvdbll3pv.onion

This is a TORv2 address and no longer up. It simply hosted an image. See backup of HTML [here](./auqgnxjtvdbll3pv.html).

![1033.jpg](./1033.jpg)

# Outguess

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Welcome.

Good luck.

3301



e = 65537
n = 75579125746085351644267182920580212556413102071876330957950694457000592\
    10248050757270234679993673844203148013173091173786572116639


- -----BEGIN COMPRESSED RSA ENCRYPTED MESSAGE-----
Version: 1.99
Scheme: Crypt::RSA::ES::OAEP

eJwBswBM/zEwADE2MgBDeXBoZXJ0ZXh0LE2jxJS1EzMc80kOK+hra1GKnXgQKQgVitIy8NgA7kxn
2u8jNQDvlu0uymNNiu6XVCCn66axGH0IZ9w4Af3K/yRgjObsfA1Q7QqpXNALJ9FFPgYl5rh07cBP
M9kbSH6DynU/5cYgQod2KymjWcIvKx3FkjV4UOGakDnBf1eQp1uwvn3KxDVwTyzPqbMnZvOA06Ec
AfKtyz1hEK/UBXkeMeVrnV5SQQ==
=yTUshDMKN65aPaKAR0OU8g==
- -----END COMPRESSED RSA ENCRYPTED MESSAGE-----


-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJSyly/AAoJEBgfAeV6NQkPHhUP/R7nuYiTMw+3sbe0xV+4rmiN
liSDmW6ibOK4UTkZDTeAS5kAKIjxCC3DwWi0lXqBGZyabojWHM2wRwYLOhvfKvgg
DgPnW1BSZ/R67GaUy0CM/vtZOtktBeIdntlZamk9DpW5bQ311c7N9dy6uWc8+hOM
umkcnT7u799zESazFgCeDSOw0cFgHDiG9UTAQxbe+NsXY/NKm4N0WAtgWmdte5ym
dU8ImpmXWg8NChdn49UtuAACi8s8tcI/lHj1Yjh+AQRbO2+Ozn9eSxUAQ1TsXSgt
30jKmXI5ss4WHS16nYsS97BUbo4oX3NBXaCjSZb7fKO9CRJBo3gm2R8/NcIMIkEc
GlQ/7rCQWHXA0MC+415ut5dcJf2ihwid81c1xsDyqQdfhEsWE/wVnK7Ujje+BgcO
ybBHl8ejJzWhZkCvesHOmIo1RLEanxlGUC5jcRLqImrT7A9CrO+EVFW16EZpvzug
Tsopo56+JbIFiIzAq+CGujHgDZnoHJFtB574utjOnZz9xzsVZ3lirQyAFOGauH+g
K+XxjXjY8tT5lppAgmF3zWKqha7NoV+9FgFl2q2SS9ue+s4Joyn5PYKnICJeze3i
K9BZ7gIT694s4dLEzu6kGaRyuNmx8qaoDs0kjvEB5pI+1buGuNAysHQWIDyY3DWb
CjJ1AnBLY0ObxaMbWMR/
=d5E8
-----END PGP SIGNATURE-----
```

## Solving

This puzzle is very similar to the [2012 RSA challeng](../../2012/008-rsa-emails/README.md#challenge). We will have to factor `n` int `p` and `q` and decrypt the RSA message.

See [factor.sh](./factor.sh) for doing so, it will run `cado-nfs` in a docker container and factor for several hours to a day+ depending on computing power. 

After the GNFS completes we receive `p` and `q`.

```
...
97513779050322159297664671238670850085661086043266591739338007321 77506098606928780021829964781695212837195959082370473820509360759
```

**Recreating the private key**

I have included [recreate-pk-decrypt](./recreate-pk-decrypt.pl) to recreate the private/public keys at [numbers.private](numbers.private) and [numbers.public](numbers.public). I have also created an ASCII armored version of both with [recreate-armor.py](recreate-armor.py) at [armored.pem](armored.pem).

You can run the whole chain with [solve.sh](solve.sh).

```
$ ./solve.sh 
-----BEGIN COMPRESSED RSA ENCRYPTED MESSAGE-----
Version: 1.99
Scheme: Crypt::RSA::ES::OAEP

eJwBswBM/zEwADE2MgBDeXBoZXJ0ZXh0LE2jxJS1EzMc80kOK+hra1GKnXgQKQgVitIy8NgA7kxn
2u8jNQDvlu0uymNNiu6XVCCn66axGH0IZ9w4Af3K/yRgjObsfA1Q7QqpXNALJ9FFPgYl5rh07cBP
M9kbSH6DynU/5cYgQod2KymjWcIvKx3FkjV4UOGakDnBf1eQp1uwvn3KxDVwTyzPqbMnZvOA06Ec
AfKtyz1hEK/UBXkeMeVrnV5SQQ==
=yTUshDMKN65aPaKAR0OU8g==
-----END COMPRESSED RSA ENCRYPTED MESSAGE-----
e: 65537
p: 97513779050322159297664671238670850085661086043266591739338007321
q: 77506098606928780021829964781695212837195959082370473820509360759

d: 4732964431916457751853715388625558850004959217132118496185749196847477596607397581953954592744686583937690489641508827925187457553
n: 7557912574608535164426718292058021255641310207187633095795069445700059210248050757270234679993673844203148013173091173786572116639
phi: 7557912574608535164426718292058021255641310207187633095795069445525039332590799817950740043973307781280290968047454108226724748560

Key check: OK
Plaintext: cu343l33nqaekrnw.onion
```
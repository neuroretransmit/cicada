# xsxnaksict6egxkq.onion

After receiving the second onion from the [`TCP Server`](../004-first-onion/README.md#tcp-server), solvers headed over to its webpage. They were greeted with a familiar message.

See [patience.html](patience.html) for the webpage.

```html
<html>
	<head><title>3301</title></head>
	<body>
		Patience is a virtue.
		<!-- which means, come back soon. -->
	</body>
</html>
```

## The leak

After a solver tried to Telnet into the server, it errored and the VPS IP was leaked. 3301 promptly took it down. `http://li528-4.members.linode.com/` was working on plainweb just fine until TOR 2 ver 1 went down.

```
$ nc -x localhost:9050 xsxnaksict6egxkq.onion 80
abc
---------------------------------------------------------------
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>501 Method Not Implemented</title>
</head><body>
<h1>Method Not Implemented</h1>
<p>abc to /index.html not supported.<br />
</p>
<hr>
<address>Apache/2.2.22 (Ubuntu) Server at li528-4.members.linode.com Port 81</address>
</body></html>
```

## Site back online

When the site returned, the following hint was displayed. See [everything-you-need.html](everything-you-need.html) for the site.

See [everything-you-need.txt.asc](everything-you-need.txt.asc) for the signed message.

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

You already have everything you need to continue.

Sometimes one must "knock on the sky and listen to the sound."

Good luck.

3301

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJQ85gbAAoJEBgfAeV6NQkP6joP/iHzBMvK6YZO24wv24RtstGJ
dEMrC9BjtUhrB+F0++sHqWeYuueZ37bDstIoh6EOenRHpECD0QBPTc40aUl2Op1L
4NuUVCUQvfqo/kdWBmSdTP4xGoCtwcXoISfhSM/i+wXqRONSy4z0FrXA3N9yxFaK
eqlNk47aZvyWWHcyYACUEar/V4kfGo8j58r2CisnfeNwat6I6ZfL9P370UVJQyG1
a0WV7rF015TLbwAJkwI1jX7GLPWOkRK3lP8qLJJodNvMPSSyUPyPB01ElgBopm+t
U9bQb/wIGtGG74ezUvwhtDGtXJLWllZtrZx82mQQWzzn8hReqqX0T35idJlTfxIz
aZDNjLCOQJZCngmXEN7iz47w/g67BQ5eoa6iEj7blFwzMwVO7M7pL+L6LZLnuXml
Zv1oDNCuENrIo4j8VGLro9pLptiilsUA6xFRS9bfE7qeeBfmS4J8DScOddzLYNVv
5fKd6iaLJoAqJGkcKnAWPl5VViDhYRL0z1N80zpjm1cWtPBIS2odLMZT80VfMYQI
8XXaEmRqoP8/9EImapqeSk+qcrUkT1+2opKRTOf7754ptjvJq31jQJgeY2gKGtp1
jPXZiu9Pp3QQ5cRKIWIIdOFvcrVtIZ/P3OYhT0p4Z+L13fScUbr/kxI6KcZmY/1D
Szqzyr8SW7zRz1ypGffc
=UPkJ
-----END PGP SIGNATURE-----
```

## ICMP/Ping puzzle

The hint from the previous section is instructing users to "knock" or use ping. The pong responses had data appended to them, hex yet again.

The full puzzle can be solved with [icmp.sh](./icmp.sh)

```
d2eda7698b2057681c3846fba7bf4b1c1bc6c7f2e8db8fc

17:32:40.975445 IP (tos 0x0, ttl 50, id 16499, offset 0, flags [none], proto ICMP (1), length 84)
    li498-122.members.linode.com > xxxx: ICMP echo reply, id 54023, seq 1011, length 64
E..T@s..2...j.gzX...........hL.PN.
..
.................. !"#$%&'()*+,-./01234567

17:32:40.976024 IP (tos 0x0, ttl 50, id 0, offset 0, flags [DF], proto ICMP (1), length 84)
    li498-122.members.linode.com > xxxx: ICMP echo reply, id 3461, seq 1, length 64
...e0ddd275cf4069985ed481c22491bb267414e5fb128fdb429c662443

17:32:41.975507 IP (tos 0x0, ttl 50, id 16500, offset 0, flags [none], proto ICMP (1), length 84)
    li498-122.members.linode.com > xxxx: ICMP echo reply, id 54023, seq 1012, length 64
...T@t..2...j.gzX...........iL.P
..
.................. !"#$%&'()*+,-./01234567

17:32:41.976238 IP (tos 0x0, ttl 50, id 0, offset 0, flags [DF], proto ICMP (1), length 84)
    li498-122.members.linode.com > xxxx: ICMP echo reply, id 3463, seq 1, length 64
...f6856ed2d4aa87f36686ca58e0f82927b1756e6d7bcf94f6abb55c4f
```

In total, the hex looked like this (see [icmp-echo.txt](./icmp-echo.txt)).

```
1f8b080843f5ee5000036d6573736167652e7478742e617363006d93
49b3aa460085f7fd2b582645dd8b80a2bcaa2c804668440691417620
202d43338bfefadc57c92e39db337cabf3f5f52359d59045399a4379
48b354489d55cf9334f5b7f705f4642c7f519e2eb1008030af6b2a23
6dfe4d5137325365b2e4d49d34395524c337005d55372b97e7a5503c
a7fda7f8262d262d001a211955cff7ea27c3f39bdf535fff454b57ff
f22f35c887f1a7f98bd2dad9d1a885fdde7eb32cf58766f98c89db79
fd1300eca2bb2ca9b2f49034d935dcfd12404922862a3f0a290f04cb
ad1c71dd3a0ccf4a3bd3f9a0b2c2f830cacf3958d1dd6ec1f674746d
7a0e82f1b2e33fa8f1fabaec051c48aa489fc87e41fd1372aff28afc
63708b2db96744eea5c6c6ac78a4258b0ef4fe165f5d5c224fcc6817
ce2fdf5aa2618bebe1d2a0ebe93c842f1e72fcd085a310d76d5ece3e
0cd0616e534b8c315f02be5c48c533347324858913f1b4a4843e2288
f757d1b22e5d9f778f286384cc45ceb66a05be3a290eb771cfd9a5e0
8ae8086273dd49d063b7f6925847cb97f4abc1f659e5dceed9155bd0
a8d6be62c703f7e632a211d5d928a5ec1b6bfd3e633f885ac062d37e
35dcc91a0a0115c2f6b4aa249fec2109fb87e808352f3fb5c051aa81
4cb2b03978dec899b81c93adbcc105e27920c975b778103d3a79663e
c866c2e3cd2eda7698b2057681c3846fba7bf4b1c1bc6c7f2e8db8fc
e0ddd275cf4069985ed481c22491bb267414e5fb128fdb429c662443
f6856ed2d4aa87f36686ca58e0f82927b1756e6d7bcf94f6abb55c4f
96cef7019c7a73f7d6bdb643bb8d32118916def730f62f72354cec30
6d736b1d95de65a330cf98324cfb54f06ac3c81bc376d2b49940b083
7b0c7d9b1e381bf96a7c2d14ef997d86e86e1c8ee6d42b5a909846a9
64e31b0f17bdf12fafea66be18f970edee86fb017d7a13480e574846
94aac25c422be02ec1a9e9c2de84e7d2d4f4e059c1a7d1914cdd99bc
9da6ef3a9c2fad5e1cfbe2a403b699d3e52c6964c30feb5adf6831d2
c05f82f718fff9896ac1ff7bc9df603740d3bf030000
```

This is decoded the usual way, albeit without offsets. The result is a gzipped PGP message. (see [decode-hex.py](decode-hex.py))

See [icmp-echo.asc.gz](icmp-echo.asc.gz) for the archive and [icmp-echo.asc](icmp-echo.asc) for the message.

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1


Well done.  You have come far.

pklmx2eeh6fjt7zf.onion

Good luck.

3301


-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJQ7vVDAAoJEBgfAeV6NQkP9x4P/31A5LPzIhkii8sBjuVxIcOn
4KFQO+uVVsR53zImSqlhq6iVAE9+Ko7vIqjD2whTIUFVYZNBq/92wEZJuCSonovH
HqYZTQihIS9d+QDuwUNvXr4ilrRmITKMrWw3D23rpWs6ZlnehuUDVI8unbN9Zi3h
3hvok3/+/FofLia9Kvbo+FIDi7T9NNRpqepgXd/6dQIP4kn63kKCP20QMdRf2fXF
ZLx5ADS14OvaNFNUAHTJ1qdkPYcdTiNDJkxqk1s82y2doGoEP0ChBUJxlyMiUVXn
1iLOwm2KNrf6If64KxEoetOraWqg9P6l3BjGVPCkrotB608SSs2Lihsa4B0ifI33
ABlpvSDIgpBu/zIO/WFYOfnnrtdvDpVP/Wy+pgqZJ/wOUuhJZhzi5vppjVCm/q9H
C/aXQxa+XXe7his4f9tuIBD1wIYAtnE8M0uDCsfiZjBaZNMnOO7/hOwnNQSBAMcr
KqL5yHSnpI50CtoA+6ycWZURBkrt1rt4eNxsCqQ1XWed/hWbqb6SlJJemJOPbbmt
V5D7iDUO+r2OIUEZTfCSjdzrXcJ8FLtqCGVaLJhCdsyirRHmURwkYLw/B8TpcJQz
qbY6oeDxDosIbE6uhDNV2RVKmpWqLDMhLGHVjkDjJpodE5L3ObbylWuRnHfFqfKH
1mubvMAGo03rxxlY+9XG
=6Sgs
-----END PGP SIGNATURE-----
```
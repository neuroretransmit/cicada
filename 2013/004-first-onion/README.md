# Onion

Using the solve of the [twitter](../003-twitter/README.md#twitter)'s many chained puzzles message we were led to an onion.

```
Come to emiwp4muu2ktwknf.onion
We shall await you there.
Good luck.
```

## emiwp4muu2ktwknf.onion

After users visited the onion, they were greated with this message - signaling another protocol must be used.

I've recreated the blank html site in [emiwp4muu2ktwknf.html], not much is known about the HTML in terms of title, etc. Only its intial page.

```
Web browsers are useless here.


      ,+++77777++=:,                    +=                      ,,++=7++=,,
    7~?7   +7I77 :,I777  I          77 7+77 7:        ,?777777??~,=+=~I7?,=77 I
=7I7I~7  ,77: ++:~+7 77=7777 7     +77=7 =7I7     ,I777= 77,:~7 +?7, ~7   ~ 777?
77+7I 777~,,=7~  ,::7=7: 7 77   77: 7 7 +77,7 I777~+777I=   =:,77,77  77 7,777,
  = 7  ?7 , 7~,~  + 77 ?: :?777 +~77 77? I7777I7I7 777+77   =:, ?7   +7 777?
      77 ~I == ~77= +777 777~: I,+77?  7  7:?7? ?7 7 7 77 ~I   7I,,?7 I77~
       I 7=77~+77+?=:I+~77?     , I 7? 77 7   777~ +7 I+?7  +7~?777,77I
         =77 77= +7 7777         ,7 7?7:,??7     +7    7   77??+ 7777,
             =I, I 7+:77?         +7I7?7777 :             :7 7
                7I7I?77 ~         +7:77,     ~         +7,::7   7
               ,7~77?7? ?:         7+:77777,           77 :7777=
                ?77 +I7+,7         7~  7,+7  ,?       ?7?~?777:
                   I777=7777 ~     77 :  77 =7+,    I77  777
                     +      ~?     , + 7    ,, ~I,  = ? ,
                                    77:I+
                                    ,7
                                     :77
                                        :

Welcome.
```

### TCP server

Using the hint, solvers found that they could use one of a number of ways to connect to the server using raw TCP sockets. I have recreated this server [here](./server.py) with what is publicly known.

You are greeted with the following prompt as the HTML page:

```bash
$ nc localhost 80
Web browsers are useless here.                                                  
                                                                                
                                                                                
    ,+++77777++=:,                    +=                      ,,++=7++=,,       
  7~?7   +7I77 :,I777  I          77 7+77 7:        ,?777777??~,=+=~I7?,=77 I   
=7I7I~7  ,77: ++:~+7 77=7777 7     +77=7 =7I7     ,I777= 77,:~7 +?7, ~7   ~ 777?
77+7I 777~,,=7~  ,::7=7: 7 77   77: 7 7 +77,7 I777~+777I=   =:,77,77  77 7,777, 
= 7  ?7 , 7~,~  + 77 ?: :?777 +~77 77? I7777I7I7 777+77   =:, ?7   +7 777?      
    77 ~I == ~77= +777 777~: I,+77?  7  7:?7? ?7 7 7 77 ~I   7I,,?7 I77~        
     I 7=77~+77+?=:I+~77?     , I 7? 77 7   777~ +7 I+?7  +7~?777,77I           
       =77 77= +7 7777         ,7 7?7:,??7     +7    7   77??+ 7777,            
           =I, I 7+:77?         +7I7?7777 :             :7 7                    
              7I7I?77 ~         +7:77,     ~         +7,::7   7                 
             ,7~77?7? ?:         7+:77777,           77 :7777=                  
              ?77 +I7+,7         7~  7,+7  ,?       ?7?~?777:                   
                 I777=7777 ~     77 :  77 =7+,    I77  777                      
                   +      ~?     , + 7    ,, ~I,  = ? ,                         
                                  77:I+                                         
                                  ,7                                            
                                   :77                                          
                                      :                                         
                                                                                
Welcome.   
```

### Commands

**`help`**
```
help
help, [number] (or number [number]), count [phrase], hello
```

**`number <num>` or `<num>`**

The `number` command had different responses depending on the properties of number provided.

1. If the number was prime, and the number reversed was prime it would reply with a `+`.
2. If the number was prime, and its reversal was not prime it would reply with the reversal's factors.
3. If the number was not prime, it would print its factors.
4. If the number is greater than `0xffffffffffffffff`, the response was `0 0`

```
3301
+
number 283
382 : [1, 2, 191, 382]
222
222 : [1, 2, 3, 6, 37, 74, 111, 222]
222222222222222222222222222
0 0
```

**`count <word or phrase>`**

The `count` command would give the [gematria](../003-twitter/README.md#gematria) value of the word. It sums the numerical value of each letter. Based on the type of number, you had special characters added to your numbers.

1. If the number was prime, and the number reversed was prime it would append a `+`.
2. If the number was prime, and its reversal was not prime it would append a `*`.
3. If the number was not prime, it would simply print the number.

```
count the instar emergence
761+
count parable
449*
count yung innanet
526
```

**`hello`, `hi`, `get message`, `get 3301`, `get 1033`**

```
hello
A message for you:

0000000:2d2d2d2d2d424547494e20504750205349474e4544204d4553534147452d2d2d2d2d0a486173683a20534841310a0a20202020200a5665727920676f6f642e0a20
0000041:20200a596f75206861766520646f6e652077656c6c20746f20636f6d652074686973206661722e0a20200a7873786e616b73696374366567786b712e6f6e696f6e
0000082:0a20200a476f6f64206c75636b2e0a2020200a333330310a20202020200a2d2d2d2d2d424547494e20504750205349474e41545552452d2d2d2d2d0a5665727369
00000c3:6f6e3a20476e7550472076312e342e31312028474e552f4c696e7578290a0a69514963424145424167414742514a513653304841416f4a45426766416556364e51
0000104:6b502f4a3051414c44716133564a7939784c4c6c6749356a5068524970340a66786562624e6874454c4f4859466b44355a397a745159476c65376c4b504d386c6b
0000145:4d536e636949593035394b4969354e53545637493937734a626f473377740a6b6848745a674e52773176325751357575724375356c31772b38342f4c354a7a324e
0000186:6d456c784f427a57723638646c5159743271664251786b327a522f6654490a544c43454776465a746c6e724e66426b376a7349794a59635858506761625334376f
00001c7:5039764f45586c42312b506d30433775505042504e3761716b665550476c0a6f3166326873634a66374a65324476625a742b3665787859736d3537467039353358
0000208:414e41642f557046567a542f3835325867363367745a72492b536d66335a0a4256636a70437a7948337753385230694d2b7270303243774a704a7a7357474c7865
0000249:51476d584c325358424234337a565a414a716c355564584c5447586b62640a6e504d64332f43624a2b6c37724f305941673570334a66344b617558375a64365a63
000028a:3277484b4c4f76666a5176455758495931434d68493638426a30725a6f2f0a4d2f666933313346465450416d3678684b52762f74482f387756726172326a593777
00002cb:6e45385878685273793734415a35477141326f484d6566544171335975570a35505838733638324a34706b44554b48476134793635766a49703136706d45496e4d
000030c:414c4a4762777a366d7461754251716c53364152735166656b446e336f5a0a796f73532b675743336a6449764835733557555147566c376a797a3974342b335467
000034d:35635439526e367058324e564e585378677a585842346e493258727259610a346b517235615742386c737361763372796a3543673246486c312b4d4b4f30675976
000038e:2f554633515437354d6978514d75344d2b3577436e4e656b676675794f360a5a7679627a70347334537a526a6b6b39734d4d360a3d5759564f0a2d2d2d2d2d454e
00003cf:4420504750205349474e41545552452d2d2d2d2d0a
Offset: 3301, Skip: 0, Col: 65, Line: 16.
```

**`clue`, `hint`, `get hint`**

```
clue
Here is a clue:

0000000: 1fd9d91c746f141803d010071f18f0028a0b69763d1d19037daa222b4f46b3264d21ed1d31c514982b502e558ffe583b2e018e62bfe44ac063caf344469c53c7da
0000041: 72beefe909de045a3df0e8b7320d570516b431c42f73c08e39af504fd00e88bb323ae09f436395fe1955dd99251693a5971a1738871354ebebf6e74f94b21f7a3b
0000082: 346063d15bd2f0fbacc86d74b6aaaac0d44b6c54300b5eabb9d699f854ae855385fb5bce0a4304964bf6a9020acb540921d17844f39856a97a2f2623547c61009a
00000c3: 421b1756748009c31b9311745f5a2e661175c8b7958fe459fae4d96e9323b29fd21f83565c60f69d51da75ddaf6f06283b77fc0362ba41e570e70a6b6efa2a34b0
0000104: d9f1d2dde221bf636d9c7c47b6291d4bf7b3389916c46652edf7daf8efa2d0d0909f96b57a3310a3c029da90481eeb4b0d53620be26ab5fb5370bfd4edc49514b2
0000145: 2c43c402fc58554b1556d092d7410fb5cd8ba8d92af3cbbc023f3787c3ece9afee71cef31d63b826bd2292bfac22c6e5cc034237575f1737e2aa24262deced106b
0000186: 89e2032ebe6ab51c8d0cf0fe2394b0c5c8d609b1c54bd2178631f9c0f2350d7a798e52b44a50517bc0dd245db004fe0ca6460c02e81699fdea7494165c96ed4bfd
00001c7: 45d26598bf08c3d8e5486ead896f29bd0b996515157448132ea6e02f8f9d23108e69874956fdf69f2ced112f1a4924c8ec35182253c5288be0e3aa2ccbf7b7affc
0000208: d1dc90726bb30c26d41f5854a41b2ea0dc68345aa3bb11b8688c407d36cdd4cdde47d26348d75397e1636b06dbae541452c1173b59b70bc37fe28615c5636158a0
0000249: 38ab6ba758d90d2b93402505265e8374a7f5d9a7528837aad79d8e6ca20b8deac1a67755b7db9f79835a463bce04ded91a13d72c57950d95fd2f65d207299596f1
000028a: 82d27d220e44a4f95d1abb5ad1d133133b4c787721c0a3ddd32c311ffb6d8b8bc9df64658c9156bd0c1393a35236ecb18cdb93cfa5c23ccee333704fe1606fa063
00002cb: 2307b427788df8036c164ce171d42fd3d0fded1bbd8690bff52e35536a3aaaf9fa6872178f94b35b056e860d637c81664a1e1310df56344ddf19bf4fa4f2a28193
000030c: dc34cdd5423ef2cbe680fbc015ce9f6cd71424789674424ef787a1e7aec7f22d487af53bfe5e4ed4b8f207279573f00c7270e136095eb70fe6c465e0291297d059
000034d: 376088f46e159efee300d64eea644a6b5a7038f411d0f4efd67446836860f1084a01e180bacec753403fe6a845e02f82f7781eba82d2dfb38274c156f7b546cb19
000038e: b4ba5b8e84f85645830eeb3d70207d299b649e8d592536e4df0b03888ca3740d9de623d00aea1e0adfcf23d92c6dde711d187ca9d592c31ab00ac6e217892ccefd
00003cf: 1be10b
Offset: 0, Skip: 0, Col: 65, Line: 16.
```

**`cicada`, `adacic`**

```
cicada
+
adacic
+
```

**`primes`**

The `primes` command had a few interesting things going on.

1. Double spaces at `29` and `3257`.
2. Missing primes from `73` and `1223`

```
primes
2 3 5 7 11 13 17 19 23 29  31 37 41 43 47 53 59 61 67 71 1229 1231 1237 1249 1259 1277 1279 1283 1289 1291 1297 1301 1303 1307 1319 1321 1327 1361 1367 1373 1381 1399 1409 1423 1427 1429 1433 1439 1447 1451 1453 1459 1471 1481 1483 1487 1489 1493 1499 1511 1523 1531 1543 1549 1553 1559 1567 1571 1579 1583 1597 1601 1607 1609 1613 1619 1621 1627 1637 1657 1663 1667 1669 1693 1697 1699 1709 1721 1723 1733 1741 1747 1753 1759 1777 1783 1787 1789 1801 1811 1823 1831 1847 1861 1867 1871 1873 1877 1879 1889 1901 1907 1913 1931 1933 1949 1951 1973 1979 1987 1993 1997 1999 2003 2011 2017 2027 2029 2039 2053 2063 2069 2081 2083 2087 2089 2099 2111 2113 2129 2131 2137 2141 2143 2153 2161 2179 2203 2207 2213 2221 2237 2239 2243 2251 2267 2269 2273 2281 2287 2293 2297 2309 2311 2333 2339 2341 2347 2351 2357 2371 2377 2381 2383 2389 2393 2399 2411 2417 2423 2437 2441 2447 2459 2467 2473 2477 2503 2521 2531 2539 2543 2549 2551 2557 2579 2591 2593 2609 2617 2621 2633 2647 2657 2659 2663 2671 2677 2683 2687 2689 2693 2699 2707 2711 2713 2719 2729 2731 2741 2749 2753 2767 2777 2789 2791 2797 2801 2803 2819 2833 2837 2843 2851 2857 2861 2879 2887 2897 2903 2909 2917 2927 2939 2953 2957 2963 2969 2971 2999 3001 3011 3019 3023 3037 3041 3049 3061 3067 3079 3083 3089 3109 3119 3121 3137 3163 3167 3169 3181 3187 3191 3203 3209 3217 3221 3229 3251 3253 3257  3259 3271 3299 
```

The missing primes:

```
   73     79     83     89     97     101    103    107    109    113 
   127    131    137    139    149    151    157    163    167    173 
   179    181    191    193    197    199    211    223    227    229 
   233    239    241    251    257    263    269    271    277    281 
   283    293    307    311    313    317    331    337    347    349 
   353    359    367    373    379    383    389    397    401    409 
   419    421    431    433    439    443    449    457    461    463 
   467    479    487    491    499    503    509    521    523    541 
   547    557    563    569    571    577    587    593    599    601 
   607    613    617    619    631    641    643    647    653    659 
   661    673    677    683    691    701    709    719    727    733 
   739    743    751    757    761    769    773    787    797    809 
   811    821    823    827    829    839    853    857    859    863 
   877    881    883    887    907    911    919    929    937    941 
   947    953    967    971    977    983    991    997    1009   1013 
   1019   1021   1031   1033   1039   1049   1051   1061   1063   1069 
   1087   1091   1093   1097   1103   1109   1117   1123   1129   1151 
   1153   1163   1171   1181   1187   1193   1201   1213   1217   1223
```

There several randomized, classic computing error messages and other quirks - but they are out of the scope of what is relevant for solving.

## Solving

Using the information from the TCP server, we can now begin to solve this step.

*Note: full solve available in [solve.sh](solve.sh).

For both of these steps, we will be using the [./decode-hex.py](script).

### `clue`

After decoding the `clue` command, the file is random data. Following the queue from previous puzzles, XORing it with [_560.00](../002-3301/3301-contents/data/_560.00) in the `data/` directory of the [OS](../002-3301/README.md#3301)

See `xor-clue.sh` for a scripted version of this.

```
$ file clue.txt.bin
clue.txt.bin: data
$ ../003-twitter/xor.py clue.txt.bin ../002-3301/3301-contents/data/_560.00 clue.txt.bin^_560.00.bin
$ file clue.txt.bin^_560.00.bin 
clue.txt.bin^_560.00.bin: PGP signed message
```

See [clue.txt.asc](clue.txt.asc).

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

  
   
You can't see the forest when you're looking at the trees.
     
Good luck.
   
3301
  
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJQ6SnrAAoJEBgfAeV6NQkP8k0P/21iHNB+ON8i8VkPbepPap6A
HIFPqGPMBZTYeuteVmHRgi+HhXPXypkWKyDM23oXbit6xXxSfK/h/FtQSPz3TS/R
i580OvFRIzRiLcs+AhMQano/JD+zp8vwtI/V6ZYedrf6Kfv0w/VOb4NW1bIv3mrU
Z12ORUrbsfzgKZMUGx6hTaTdc7ZcAAmWkFOtwsYBXVfwe1bmEE5BfnkdehyKTEuu
2WIAZluHd/J0kbngwYqMt6JHk17of6ewpoNHzVcAnA6IA5uB0n2P/6uJ8bFneMoH
ybyw7iSBEu3ixg0xaXCpWghr34jGc66HCSz6RKA6dwiN+CFoS8lEwMg94BjGc2MT
FZ8tOopB8Qg2+RpA2KegItZxBpWGMXBKqZM1+mRuVZU30BxhidmHN39wRlQ2Tu4V
n6RqAIOZhNctb6Kujx+1ujGkN90x9xHmhL8ik2FIrYRylX2a8PtmkgajO3y1fP0X
NKAPNimClJb/NZED7Wcjv2h7OBNyKdk7D1xjSXd3d7euxoENr4edetcQ8npVLEow
RJbJhznxeu5D/qNU6lse6y39EPFrpFDoMbpds7e7WvKcHeSorzcQGkRtYigoMsX3
KmQPKiiQYvinfBbu9qHR6FXmyIPfio4ncgxSV23mt11zYwJh/IBXkdVBnZIP6aZs
SEKC3iyNQLA8bppBZ+kk
=6gnK
-----END PGP SIGNATURE-----
```

### `hello`

Simply decoding the hex left us with the following message, it has whitespace like many other messages.

See [hello.txt.asc](hello.txt.asc).

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

     
Very good.
   
You have done well to come this far.
  
xsxnaksict6egxkq.onion
  
Good luck.
   
3301
     
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJQ6S0HAAoJEBgfAeV6NQkP/J0QALDqa3VJy9xLLlgI5jPhRIp4
fxebbNhtELOHYFkD5Z9ztQYGle7lKPM8lkMSnciIY059KIi5NSTV7I97sJboG3wt
khHtZgNRw1v2WQ5uurCu5l1w+84/L5Jz2NmElxOBzWr68dlQYt2qfBQxk2zR/fTI
TLCEGvFZtlnrNfBk7jsIyJYcXXPgabS47oP9vOEXlB1+Pm0C7uPPBPN7aqkfUPGl
o1f2hscJf7Je2DvbZt+6exxYsm57Fp953XANAd/UpFVzT/852Xg63gtZrI+Smf3Z
BVcjpCzyH3wS8R0iM+rp02CwJpJzsWGLxeQGmXL2SXBB43zVZAJql5UdXLTGXkbd
nPMd3/CbJ+l7rO0YAg5p3Jf4KauX7Zd6Zc2wHKLOvfjQvEWXIY1CMhI68Bj0rZo/
M/fi313FFTPAm6xhKRv/tH/8wVrar2jY7wnE8XxhRsy74AZ5GqA2oHMefTAq3YuW
5PX8s682J4pkDUKHGa4y65vjIp16pmEInMALJGbwz6mtauBQqlS6ARsQfekDn3oZ
yosS+gWC3jdIvH5s5WUQGVl7jyz9t4+3Tg5cT9Rn6pX2NVNXSxgzXXB4nI2XrrYa
4kQr5aWB8lssav3ryj5Cg2FHl1+MKO0gYv/UF3QT75MixQMu4M+5wCnNekgfuyO6
Zvybzp4s4SzRjkk9sMM6
=WYVO
-----END PGP SIGNATURE-----
```


# Twitter

In the 3301 [OS](../002-3301/README.md#usrlocalbin) there was a message pointing to a Twitter handle [@1231507051321](https://twitter.com/1231507051321).

## Code

The account was tweeting from a bot account using a different source, `1033` (client label, i.e. TweetDeck, Twitter Web Client, etc.). See [0.json](tweets/0.json) for clarity. At the time of writing this the Twitter API only provides 200 tweets at a time, even the search API bypass no longer works. For historical reference, I'm basing this only off of what I was able to acquire with the limitations.

The bot was tweeting out a code at an interval of 2 seconds between what I'm able to query, see [times.py](times.py) for verification. According to Nox's video, it sounds like the dump halted somewhere in the middle of the data.

The code was of the format `offset: data`, where the data was encoded in hex. See [full.txt](tweets/full.txt) for the full listing of tweets in reverse order.

Example: 

```
0000000: b69ccce300104a464802545959580001008d0000ff8b6131616a6a632737293d3e322b3b3e3f263a203c0c4762677c326767713d73716d697b6e3000505b494e47
```

There was a final tweet stating the following hint:

```
Offset: 0, Skip: 0, Col: 65, Line: 988
```

### Solving

This puzzle could be solved in two ways, one required the full text dump from the Twitter and the other required using the XOR function to get the data without it being posted using pieces from the [OS](../002-3301/README.md#3301). I will demonstrate the latter.

*Note: See [twitter.sh](twitter.sh) for single script to execute all that is below.*

For each line in the code, the hex needs to be decoded to binary and written into a file at the specified offset. For this, I have written [decode-tweets.py](./decode-tweets.py). The output file is [twitter.bin](twitter.bin) - which is random garbage until we XOR with others to get something useful.

```bash
$ file twitter.bin
twitter.bin: data
```

To get our first useful intermediate component, we must XOR [560.13](../002-3301/3301-contents/data/560.13) with [761.mp3](../002-3301/3301-contents/audio/761.mp3). Using this result, we must XOR it (see [xor.py](xor.py)) with the [twitter.bin](twitter.bin) from the previous step resulting in ASCII text. The result is half base64 and half a repeating pattern divided by dashes. See [b64.txt](b64.txt).

```bash
$ CONTENTS="../002-3301/3301-contents"
$ ./decode.py
$ ./xor.py "$CONTENTS/data/560.13" "$CONTENTS/audio/761.mp3" "560.13^761.mp3.bin"
$ ./xor.py "560.13^761.mp3.bin" "twitter.bin" "b64.txt"
```

At this point, we are going to take the (short cut) long route as it is by far more impressive and cool. Split off the repeating pattern (see [split.py](split.py)). This results in [only_b64.txt](only_b64.txt) and [only_pattern.txt](only_pattern.txt). From here we will base64 decode into a PNG.

```bash
$ ./split.py "b64.txt"
$ cat "only_b64.txt" | base64 -d > decoded.png
$ file decoded.png
decoded.png: PNG image data, 521 x 523, 8-bit gray+alpha, non-interlaced
```

![decoded.png](decoded.png)

There is nothing special about this image, aside from Cicada breaking their usual JPG preference for outguess. I have found no traces of steganography with many tools. This is our final piece needed to reconstruct with XOR.

```bash
$ ./xor.py "$CONTENTS/data/560.13" "decoded.png" "560.13^decoded.png.bin"
$ ./xor.py "560.13^decoded.png.bin" "$CONTENTS/audio/761.mp3" "560.13^b64.txt.bin"
$ ./xor.py "./twitter.bin" "$CONTENTS/audio/761.mp3" "gematria.jpg"
$ file gematria.jpg
gematria.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 598x842, components 3
$ outguess -r "gematria.jpg" "gematria.jpg.asc"
Reading gematria.jpg....
Extracting usable bits:   49750 bits
Steg retrieve: seed: 17, len: 1443
```

## Gematria

A lookup table of Elder Futhark runes, English letter, and prime gematria value. Gematria is not a new subject, it has been used for Hebrew words for millenia. This is a unique gematria.

Of note, this lookup table is missing lookups for the English letters `Q` and `V`.

![gematria.jpg](gematria.jpg)

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1


 	    		 		 				 		 		 	 		  	 	  	      			 	   		 				  	      		  	 	 		 		 	 		 	  	 			 			 			      		 	   		 		 	 			 	 	 			 	 	  		  	  		 	 		 			 	   			 			 		 	 		 		 			  		  		   	 			  		 				 		 			  		 	  	 		 				 		 			 

 	 	 			 		  	 	  	      			  		 		 	    		    	 		 		   		 		    	      		    	 			 			 		    	 		 	  	 			 	    	      				  	 		 				 			 	 	  	      			 	   		 	    		  	 	 			  	  		  	 	  	 			 

 	   			 		 				 		 				 		  	    	      		 		   			 	 	 		   		 		 	 		  	 			 

  		  		  		  		  		      		   	
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJQ5lDTAAoJEBgfAeV6NQkP7nMQAJVg7DQiIA7NpkacR0RA4eBs
NZHJBQNHO2P22h+aFfP/rI1gjGaV3hMWaa2sQ4Vbi/W8eZuH40AsmZUy3EOb+4j0
3cJRJgAJI99ZjDcVXITm5VyUv+WIqCzBr+bHMK7pkMYQ/rEzeWD56tlsrDgFdjmh
PA/b7XrDcofd9JfBNFI7D/sF84HL2ig5baNo+MGjYl4Dq2cHX+SAafXmlN9PXFjx
HRBbuoMLlviKywQ8MnePBPYG6V8sIMmrJlHS5ZcNEaSJ9nGL4X0XbECqV79ermye
1EeNKcckoeeZMU86SabfMeyZozG04Vkbemn8JH5cssbuF8hf4fdN/LSP4NG0r5y9
jfRv7z59pL577ZpGAju5zBtlCBUvmxxNYR5IGLg+Fi/ICqcRC98mzesFnQ7wbDLS
HKyV95SBQK82bbqSREBfIrrNb+MjVtJwIvOY5OPTBViHPqrIuMw8KDGfSvw9ncCt
dase7vUjXxIrn36xDSRN6cMzTmFZ9lkQYkRAYq5ApERud+JfKCwszG/UxRwo1WOU
0ALaWXq5VMp+w5pvQkqg9eHpOriG9Z11VLdb53eTmxKrwyX/2eaiybsnMrRNuxv1
iE8PVRkifCcJccw1bGq8TyCQF3a5ozeiBRngAUT7BwZhLa4bShtki7amR0ZZgbKk
8JRMGvoSA5NNTEwvUhwl
=ZeNf
-----END PGP SIGNATURE-----
```

This is not an empty message, there are long lines of tabs and spaces that need to be represented as binary and decoded to ASCII. See [decode-whitespace.py](./decode-whitespace.py)

We have now completed the Twitter puzzle with the aid of [OS](../002-3301/README.md#3301) files.

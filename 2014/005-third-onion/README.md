# fv7lyucmeozzd5j4.onion

After solving the first three pages, the [columnar transposition](../004-first-three-pages/README.md#pgp-message-from-xor-of-pgp-messages-in-3-first-pages) revealed this onion address.

## Hex/status page

Logs over time are unavailable, what we do have is the final string. It is a 512 character (256 byte) string that appears to still be a loose end. 

```
<!--1033-->
87de5b7fa26ab85d2256c453e7f5bc3ac7f25ee743297817febd7741ededf07ca0c7e8b1788ea4131441a8f71c63943d8b56aea6a45159e2f59f9a194af23eaabf9de0f3123c041c882d5b7e03e17ac49be67cef29fbc7786e3bda321a176498835f6198ef22e81c30d44281cd217f7a46f58c84dd7b29b941403ecd75c0c735d20266121f875aa8dec28f32fc153b1393e143fc71616945eea3c10d6820bd631cf775cf3c1f27925b4a2da655f783f7616f3359b23cff6fb5cb69bcb745c55dff439f7eb6a4094bd302b65a84360a62f94c8b010250fcc431c190d6ed8cc8a3bfce37dddb24b93f502ad83c5fa21923189d8be7a6127c4105fcf0e5275286f2
```

Status page leaks (showing the linode address (see [here](ZRJhYgGP) and [here](je6Yudvh)). From [reports](5iRnfLkm) it sounds like the original status page was static, after it was found it sounds like it tripped an update on the new status page. the The original HTML can be found [here](li676-224_server-status_new.txt) with the huge block of hex. This hex grew over time, [see hex-growth-over-time.json](hex-growth-over-time.json) for a list of JSON objects describing this growth (taken from numinit's GitHub).

The HTML for the completed status page is [here](./li676-224_server-status_new.html).

## Hex

See [decode.sh](decode.sh) for the full process.

The hex is a large binary file with two jpegs, one at the beginning and the other at the end - reversed. 

```bash
$ xxd -r -p server-status.hex -> server-status.jpg
$ ./reversebytes.py
$ cmp -l server-status.jpg ./server-status-reversed.jpg > cmp.txt
$ dd if=server-status.jpg bs=1 count=$((0x00521e4)) status=noxfer > 03.jpg # Extract ONLY one the beginning image without OOB and reversed
```

There are some bytes between the image end bytes and the image start bytes. Both pages are the same, this is a signal to read the bytes between which are text. The offset starts at 0x00521e4 and there are 357 between.

```
$ dd if=server-status.jpg bs=1 skip=$((0x00521e4)) count=357 status=noxfer | rev | xxd -p -r > square.txt
```

See [square.txt](square.txt). The result is a magic square that sums to `1033` in all directions.

```
272     138     341     131     151
366     199     130     320     18
226     245     91      245     226
18      320     130     199     366
151     131     341     138     272
```



## Runes

![03.jpg](03.jpg)

The runes are unencrypted using the ordering from the Gematria Primus discovered in 2013. A valid decrypt will look something like this, see [gematriaprimus.py](gematriaprimus.py).

```
SOME-WISDOM.THE-PRIMES-ARE-SAC/
RED.THE-TOTIENT-FUNCTION-IS-SA/
CRED.ALL-THINGS-SHOULD-BE-ENCRY/
PTED./
&
CNOW-THIS./
272 138 SHADOWS 131 151/
AETHEREAL BUFFERS UOID CARNAL 18/
226 OBSCURA FORM 245 MOBIUS/
18 ANALOG UOID MOURNFUL AETHEREAL/
151 131 CABAL 138 272/
```

With corrections:

```
SOME-WISDOM.THE-PRIMES-ARE-SAC/
RED.THE-TOTIENT-FUNCTION-IS-SA/
CRED.ALL-THINGS-SHOULD-BE-ENCRY/
PTED./
&
KNOW-THIS./
272 138 SHADOWS 131 151/
AETHEREAL BUFFERS VOID CARNAL 18/
226 OBSCURA FORM 245 MOBIUS/
18 ANALOG VOID MOURNFUL AETHEREAL/
151 131 CABAL 138 272/
```
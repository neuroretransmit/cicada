# 232.jpg

This image was posted on 4chan's `/b/` and `/x/` boards. I've removed the filename 4chan's uploader provided and used the uploader's original name.

![232.jpg](232.jpg)

## Outguess

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Welcome again.

Here is a book code.  To find the book, break this riddle:

A book whose study is forbidden
Once dictated to a beast;
To be read once and then destroyed
Or you shall have no peace. 


I:1:6
I:2:15
I:3:26
I:5:4
I:6:15
I:10:26
I:14:136
I:15:68
I:16:42
I:18:17
I:19:14
I:20:58
I:21:10
I:22:8
I:23:6
I:25:17
I:26:33
I:27:30
I:46:32
I:47:53
I:49:209
I:50:10
I:51:115
I:52:39
I:53:4
I:62:43
I:63:8
III:19:84
III:20:10
III:21:11
III:22:3
III:23:58
5
I:1:3
I:2:15
I:3:6
I:14:17
I:30:68
I:60:11
II:49:84
II:50:50
II:64:104
II:76:3
II:76:3
0
I:60:11


Good luck.

3301

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAEBAgAGBQJQ5QoZAAoJEBgfAeV6NQkPf2IQAKWgwI5EC33Hzje+YfeaLf6m
sLKjpc2Go98BWGReikDLS4PpkjX962L4Q3TZyzGenjJSUAEcyoHVINbqvK1sMvE5
9lBPmsdBMDPreA8oAZ3cbwtI3QuOFi3tY2qI5sJ7GSfUgiuI6FVVYTU/iXhXbHtL
boY4Sql5y7GaZ65cmH0eA6/418d9KL3Qq3qkTcM/tRAHhOZFMZfT42nsbcvZ2sWi
YyrAT5C+gs53YhODxEY0T9M2fam5AgUIWrMQa3oTRHSoNAefrDuOE7YtPy40j7kk
5/5RztmAzeEdRd8QS1ktHMezXEhdDP/DEdIJCLT5eA27VnTY4+x1Ag9tsDFuitY4
2kEaVtCrf/36JAAwEcwOg2B/stdjXe10RHFStY0N9wQdReW3yAOBohvtOubicbYY
mSCS1Bx91z7uYOo2QwtRaxNs69beSSy+oWBef4uTir8Q6WmgJpmzgmeG7ttEHquj
69CLSOWOm6Yc6qixsZy7ZkYDrSVrPwpAZdEXip7OHST5QE/Rd1M8RWCOODba16Lu
URKvgl0/nZumrPQYbB1roxAaCMtlMoIOvwcyldO0iOQ/2iD4Y0L4sTL7ojq2UYwX
bCotrhYv1srzBIOh+8vuBhV9ROnf/gab4tJII063EmztkBJ+HLfst0qZFAPHQG22
41kaNgYIYeikTrweFqSK
=Ybd6
-----END PGP SIGNATURE-----
```

## Book code

```
A book whose study is forbidden
...
To be read once and then destroyed
Or you shall have no peace. 
```

### Locating the book

The first part of this message gives searchable terms to locate such a book. Knowing what is within [sacred-texts.com](sacred-texts.com) from previous browsing, a result stands out.

>The study of this Book is forbidden. It is wise to destroy this copy after the first reading. Whosoever disregards this does so at his own risk and peril. These are most dire. Those who discuss the contents of this Book are to be shunned by all, as centres of pestilence.

This result leads to [*The Book of the Law (Liber AL vel Legis)*](https://www.sacred-texts.com/oto/engccxx.htm) by Alleister Crowley. It was one of the sacred texts of his esoteric religion Thelema.

```
Once dictated to a beast;
```

From [Wikipedia](https://en.wikipedia.org/wiki/The_Book_of_the_Law):

>This is a way of saying that the book was delivered by Aiwass (whose number is both 93 and 418) to Crowley, who is The Beast 666. 

### Solving the book code

To solve this book code, a bit of parsing/text manipulation must be done prior to looking up the location references. You must split each chapter by `\d+\. ` (regex for digit-period-space). This is the numbering within the text, not necessarily a line number. Numbering within the text will be removed in this splitting. Spaces and newlines must also be replaced with an empty string.

When the preproccessing is done, you will be able to use the book code. See [boook-code.py](book-code.py) to solve the three chapters in this directory. Resulting in `https:--www.dropbox.com-s-r7sgeb5dtmzj14s-3301`. The dashes need to be replaced, finally resulting in `https://www.dropbox.com/s/r7sgeb5dtmzj14s/3301`. This link is no longer active. Dropbox previously hosted a file titled 3301.

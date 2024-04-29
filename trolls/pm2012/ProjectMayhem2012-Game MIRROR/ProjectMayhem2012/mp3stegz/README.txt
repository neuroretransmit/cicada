Application purpose:
Hide a file (of any type) inside mp3 without changing it's size and sound quality. Just try it and prove that my *stupid* algorithm works.

Features:
- hide any type of file inside mp3
- hidden file is encrypted using Rijndael algorithm
- can run on Linux machine with GUI and wine installed (actually I create this application using Delphi 7.2 under Debian GNU/Linux OS)
- the sound quality is not decreased.
- distributed with source code, you may edit it as long as I have my credit in your application.

Limitation:
- hidden file must have 3 characters file extension, so it wont work for extension such as .tiff, .mpeg, .jpeg
- not for mp3 with VBR (Variable Bit Rate), only work for CBR (Constant Bit Rate)
- the algorithm is not optimized, so it is rather slow to hide big file. Sometimes, application might look like not responding
- no documentation, no help file (just open HELP.txt for brief help)
- ugly interface

This application is created using:
- Borland Delphi 7
- DCPcrypt Cryptographic Component Library v2 Beta 3 by David Barton (http://www.cityinthesky.co.uk/)
- ZLibEx Version 1.2.3 by Roberto Della Pasqua (http://www.dellapasqua.com/delphizlib/)
All above components are free of charge. You need both component to edit this source code

There's no correlation between mp3stegz (by myself) and mp3stego (by Fabien Petitcolas). Also, mp3stegz algorithm is completely different from mp3stego, I do want to use mp3stego algorithm but I don't understand mp3stego's source code at all(it's too complicated for me to understand) so I create my own *stupid* algorithm.

Achmad Zaenuri
Author homepage: http://achmadz.blogspot.com
Author e-mail: achmad.zaenuri@gmail.com

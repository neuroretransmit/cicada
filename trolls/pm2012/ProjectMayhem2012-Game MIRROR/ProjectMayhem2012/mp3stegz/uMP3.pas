unit uMP3;

interface
uses
  SysUtils, Windows, Messages, Classes;

//mp3 header frame
type
  TRawMP3Header = record
    AudioVersion,
    LayerIdx,
    Protection,
    BitrateIdx,
    SamplingRateIdx,
    Padding,
    PrivateBit,
    ChannelMode,
    ModeExt,
    Copyright,
    Original,
    Emphasis: Integer;
  end;

//array for mp3 header frame
type
  TMP3HeaderArray = array[0..3] of byte;

//bitrate (bps) lookup table
const
  bmpeg1: array[1..14, 1..3] of Word = (
    (32, 32, 32), (40, 48, 64), (48, 56, 96),
    (56, 64, 128), (64, 80, 160), (80, 96, 192),
    (96, 112, 224), (112, 128, 256), (128, 160, 288),
    (160, 192, 320), (192, 224, 352), (224, 256, 384),
    (256, 320, 416), (320, 384, 448));

//sampling frequency(Hz) lookup table
const
  samplingRate: array[0..3] of integer = (
    44100, 48000, 32000, 0);

//sampling per frame lookup table
const
  samplingPerFrame: array[1..3] of Integer = (
    1152, 1152, 384);

function FindFirstHeader(filename: string): Integer;
function FindNextFrame(filename: string; prevHeaderPos: Integer; prevHeader: TMP3HeaderArray): Integer;
procedure ParseHeaderArray(headerArray: TMP3HeaderArray; var RawHeader:
  TRawMP3Header);
function getMP3Header(filename: string; pos: Integer): TMP3HeaderArray;
function frameSize(headerArray: TMP3HeaderArray): Integer;
function isVBR(filename: string): Boolean;
function isFirstFrame(filename: string; framePos: Integer): Boolean;
function isAvailableToSteg(filename: string; framePos: Integer; length:
  Integer): Boolean;
function isStegged(filename: string; framePos: Integer): Boolean;
function FrameCount(filename: string): Integer;
function FrameAvailableToStegCount(filename: string; length: Integer): Integer;
function MaxStegSize(filename: string; length: Integer): Integer;
function VBRPos(filename: string): Integer;
function FileSize(FileName : String) : Int64;
function HideFile(mp3File:string; hiddenFile: string; resultFile: string;
  length: Integer): Integer;
function RevealFile(mp3File:string): string;
procedure Split(const Delimiter: Char; Input: string; const Strings: TStrings);
function LeftPad(S: string; Ch: Char; Len: Integer): string;

implementation

//function to get first frame position
function FindFirstHeader(filename: string): Integer;
var
  filemp3: File;
  headerArray: array[0..3] of byte;
  count, pos: Integer;
begin
  Result:=-1;
  if FileExists(filename) then
  begin
    AssignFile(filemp3, filename);
    FileMode:=fmOpenRead;
    Reset(filemp3,1);
    //looping sampai dapat header file
    pos:=0;
    while not eof(filemp3) do
    begin
      seek(filemp3, pos);
      BlockRead(filemp3, headerArray, 4, count);
      if ((headerArray[0]=$FF) and ((headerArray[1]=$FB) or (headerArray[1]=$FA))) then
      begin
        Result:=pos;
        break;
      end else
      begin
        pos:=pos+1;
      end;
    end;
    CloseFile(filemp3);
  end else
  begin
    exit;
  end;
end;

//function to find next frame
function FindNextFrame(filename: string; prevHeaderPos: Integer; prevHeader:
  TMP3HeaderArray): Integer;
var
  filemp3: File;
  count: Integer;
  posNow: Integer;
  headArray: TMP3HeaderArray;
begin
  Result := -1;
  if FileExists(filename) then
  begin
    AssignFile(filemp3, filename);
    FileMode:=fmOpenRead;
    Reset(filemp3, 1);
    posNow:=prevHeaderPos+FrameSize(prevHeader);
    while not eof(filemp3) do
    begin
      seek(filemp3, posNow);
      BlockRead(filemp3, headArray, 4, count);
      if ((headArray[0]=$FF) and ((headArray[1] and $E0)=$E0) and ((headArray[2] and $F0)<>$F0)) then
      begin
        Result:=posNow;
        break;
      end else
      begin
        posNow:=posNow+1;
      end;
    end;
    CloseFile(filemp3);
  end else
  begin
    exit;
  end;
end;

//function for parsing mp3 header
procedure ParseHeaderArray(headerArray: TMP3HeaderArray; var RawHeader:
  TRawMP3Header);
begin
  RawHeader.AudioVersion:=(headerArray[1] shr 3) and $3;
  RawHeader.LayerIdx:=(headerArray[1] shr 1) and $3;
  RawHeader.Protection:=(headerArray[1] and $1);
  RawHeader.BitrateIdx:=(headerArray[2] shr 4) and $F;
  RawHeader.SamplingRateIdx:=(headerArray[2] shr 2) and $3;
  RawHeader.Padding:=(headerArray[2] shr 1) and $1;
  RawHeader.PrivateBit:=(headerArray[2] and 1);
  RawHeader.ChannelMode:=(headerArray[3] shr 6) and $3;
  RawHeader.ModeExt:=(headerArray[2] shr 4) and $3;
  RawHeader.Copyright:=(headerArray[2] shr 3) and $1;
  RawHeader.Original:=(headerArray[2] shr 2) and $1;
  RawHeader.Emphasis:=(headerArray[2] and 1);
end;

//function to get mp3 header of current pos
function getMP3Header(filename: string; pos: Integer): TMP3HeaderArray;
var
  filemp3: File;
  headerArray: TMP3HeaderArray;
  count: integer;
begin
  if FileExists(filename) then
  begin
    AssignFile(filemp3, filename);
    FileMode:=fmOpenRead;
    Reset(filemp3,1);
    seek(filemp3, pos);
    BlockRead(filemp3, headerArray, 4, count);
    Result:=headerArray;
    CloseFile(filemp3);
  end else
  begin
    exit;
  end;
end;

//function to find frame size
function frameSize(headerArray: TMP3HeaderArray): Integer;
var
  myRawMP3Header: TRawMP3Header;
begin
  Result:=0;
  ParseHeaderArray(headerArray, myRawMP3Header);
  Result:=trunc(samplingPerFrame[myRawMP3Header.LayerIdx]/ 8 * bmpeg1[
    myRawMP3Header.BitrateIdx][myRawMP3Header.LayerIdx] * 1000 / samplingRate[myRawMP3Header.SamplingRateIdx] + myRawMP3Header.Padding);
end;

//function to check whether an mp3 is VBR or not
function isVBR(filename: string): Boolean;
var
  filemp3: File;
  pos, n, count: Integer;
  buf: array[0..254] of Char;
begin
  Result:=false;
  if FileExists(filename) then
  begin
    AssignFile(filemp3, filename);
    FileMode:=fmOpenRead;
    Reset(filemp3,1);
    pos:=FindFirstHeader(filename);
    seek(filemp3, pos);
    BlockRead(filemp3, buf, 255, count);
    for n := 0 to 251 do
    begin
      if (buf[n] + buf[n + 1] + buf[n + 2] + buf[n + 3] = 'Xing') or (buf[n] + buf[n + 1] + buf[n + 2] + buf[n + 3] = 'Info') then
      begin
        Result := true;
        CloseFile(filemp3);
        Exit;
      end
    end;
    CloseFile(filemp3);
  end else
  begin
    exit;
  end;
end;

//function to check if certain position is first frame
function isFirstFrame(filename: string; framePos: Integer): Boolean;
begin
  Result := (framePos = FindFirstHeader(filename));
end;

//function to check if a frame contain secret data
function isStegged(filename: string; framePos: Integer): Boolean;
var
  filemp3: File;
  pos, n, count: Integer;
  buf: array[0..254] of Char;
begin
  Result:=False;
  if FileExists(filename) then
  begin
    AssignFile(filemp3, filename);
    FileMode:=fmOpenRead;
    Reset(filemp3,1);
    pos:=framePos;
    seek(filemp3, pos+36);
    BlockRead(filemp3, buf, 4, count);
    for n := 0 to 4 do
    begin
      if (buf[n] + buf[n + 1] + buf[n + 2] + buf[n + 3] = 'XXXX') then
      begin
        Result := true;
        CloseFile(filemp3);
        Exit;
      end
    end;
    CloseFile(filemp3);
  end else
  begin
    exit;
  end;
end;

//function to check if a frame is able to be stegged
function isAvailableToSteg(filename: string; framePos: Integer; length: Integer): Boolean;
var
  pos, i : Integer;
  buf: array[0..254] of byte;
  available: Boolean;
  filemp3lagi: TFileStream;
begin
  //
  available:=False;
  Result:=available;
  if FileExists(filename) then
  begin
    filemp3lagi:=TfileStream.Create(filename, fmOpenRead or fmShareDenyNone);
    pos:=framePos;
    filemp3lagi.seek(pos, soFromBeginning);
    filemp3lagi.Read(buf, length);
    for i := 0 to length-2 do
    begin
      if (buf[i]=buf[i+1]) then
      begin
        available:=True;
      end else
      begin
        available:=False;
        Result:=available;
        filemp3lagi.Free;
        exit;
      end;
    end;
    Result:=available;
    filemp3lagi.Free;
  end else
  begin
    exit;
  end;
end;

//function to count num. of frame
function FrameCount(filename: string): Integer;
var
  pos, posNext, count: Integer;
  frameHeader: TMP3HeaderArray;
begin
  Result := -1;
  pos:=FindFirstHeader(filename);
  frameHeader:=getMP3Header(filename, pos);
  count:=0;
  posNext:=pos;
  while posNext<>-1 do
  begin
    count:=count+1;
    posNext:=FindNextFrame(filename, posNext, frameHeader);
    if posNext<>-1 then
      frameHeader:=getMP3Header(filename, posNext);
  end;
  Result := count;
end;

//function to count num. of frame available for stegano data
function FrameAvailableToStegCount(filename: string; length: Integer): Integer;
var
  pos, posNext, count: Integer;
  frameHeader: TMP3HeaderArray;
begin
  Result := -1;
  pos:=FindFirstHeader(filename);
  frameHeader:=getMP3Header(filename, pos);
  count:=0;
  posNext:=pos;
  while posNext<>-1 do
  begin
    if (isAvailableToSteg(filename, posNext+36, length)) then
    begin
      count:=count+1;
    end;
    posNext:=FindNextFrame(filename, posNext, frameHeader);
    if posNext<>-1 then
      frameHeader:=getMP3Header(filename, posNext);
  end;
  Result := count-1;
end;

//function to find maximum stegano data inside an mp3
function MaxStegSize(filename: string; length: Integer): Integer;
var
  posmp3, posmp3old, n, posNext: Integer;
  firsttime, available: Boolean;
begin
  //
  Result:=-1;
  firsttime:= True;

  posmp3:=FindFirstHeader(filename);
  posmp3old:=posmp3;
  posNext:=FindNextFrame(filename, posmp3, getMP3Header(filename, posmp3));

  n:=0;
  posmp3:=posmp3+40;

  //loop until all hidden file readed
  while (posNext<>-1) do
  begin
    //happen only once
    if (firsttime) then
    begin
      if (isAvailableToSteg(filename,posmp3old+36,length)) then
      begin
          posmp3:=posNext+40;
          posmp3old:=posNext;
          posNext:=FindNextFrame(filename, posmp3old, getMP3Header(filename,
            posmp3old));
          firsttime:=False;
      end else begin
        posmp3old:=posNext;
        posNext:=FindNextFrame(filename, posmp3old, getMP3Header(filename,
            posmp3old));
        posmp3:=posmp3old+40;
      end;
    end;

    available:=isAvailableToSteg(filename,posmp3old+36,length);
    if ((available) AND (not firsttime)) then
    begin
      posmp3:=posmp3+1;
      n:=n+1;
    end else if ((not available) AND (not firsttime)) then
    begin
      posmp3:=posNext;
    end;

    if ((posmp3>=posNext) AND (not firsttime) AND (posNext<>-1)) then
    begin
      posmp3old:=posNext;
      posNext:=FindNextFrame(filename, posmp3old, getMP3Header(filename,
          posmp3old));
      posmp3:=posmp3old+40;
    end;
  end;

  Result:=n;
end;

//function to find VBR bit position
function VBRPos(filename: string): Integer;
var
  filemp3: File;
  pos, n, count: Integer;
  buf: array[0..254] of Char;
begin
  Result:=-1;
  if FileExists(filename) then
  begin
    AssignFile(filemp3, filename);
    FileMode:=fmOpenRead;
    Reset(filemp3,1);
    pos:=FindFirstHeader(filename);
    seek(filemp3, pos);
    BlockRead(filemp3, buf, 255, count);
    for n := 0 to 251 do
    begin
      if (buf[n] + buf[n + 1] + buf[n + 2] + buf[n + 3] = 'Xing') or (buf[n] + buf[n + 1] + buf[n + 2] + buf[n + 3] = 'Info') then
      begin
        Result := pos+n;
        CloseFile(filemp3);
        Exit;
      end
    end;
    CloseFile(filemp3);
  end else
  begin
    exit;
  end;
end;

//funnction to hide file inside mp3
function HideFile(mp3File:string; hiddenFile: string; resultFile: string; length: Integer): Integer;
var
  posmp3, poshidden, posmp3old, n, m, posNext, len, i: Integer;
  buff1: byte;
  firsttime, available: Boolean;
  key: string;
  streamHidden, streamHasil: TFileStream;
begin
  //
  Result:=-1;
  firsttime:= True;
  if (FileSize(hiddenFile)>MaxStegSize(mp3File, length)) then
  begin
    //exceed max size
    exit;
  end;

  CopyFile(PAnsiChar(mp3file), PAnsiChar(resultFile), False);

  //create 'key' (size and extension)
  key:=inttostr(FileSize(hiddenFile))+'#'+LeftPad(extractFileExt(
    hiddenFile), ' ', 5);
  len:=strlen(PAnsiChar(key));

  //open result file
  streamHasil:=TFileStream.Create(resultFile, fmOpenReadWrite or
    fmShareDenyNone);
  posmp3:=FindFirstHeader(resultFile);
  posmp3old:=posmp3;
  posNext:=FindNextFrame(resultFile, posmp3, getMP3Header(resultFile, posmp3));
  streamHasil.Seek(posmp3, soFromBeginning);

  //open 'to-be-hidden' file
  streamHidden:=TfileStream.Create(hiddenFile, fmOpenRead or fmShareDenyNone);
  poshidden:=0;
  streamHidden.Seek(poshidden, soFromBeginning);

  n:=0;
  posmp3:=posmp3+40;

  m:=streamHidden.Size;
  //loop until all hidden file readed
  while ((n<m) AND (posNext<>-1)) do
  begin
    poshidden:=n;
    streamHidden.Seek(poshidden, soFromBeginning);
    streamHidden.Read(buff1, 1);

    //happen only once
    if (firsttime) then
    begin
      if (isAvailableToSteg(mp3File,posmp3old+36,length)) then
      begin
          streamHasil.Seek(posmp3-4, soFromBeginning);
          streamHasil.WriteBuffer('XXXX', 4);
          for i := 0 to len do
          begin
            streamHasil.Write(Byte(key[i+1]), 1);
          end;
          posmp3:=posNext+40;
          posmp3old:=posNext;
          posNext:=FindNextFrame(resultFile, posmp3old, getMP3Header(resultFile,
            posmp3old));
          firsttime:=False;
      end else begin
        posmp3old:=posNext;
        posNext:=FindNextFrame(resultFile, posmp3old, getMP3Header(resultFile,
            posmp3old));
        posmp3:=posmp3old+40;
      end;
    end;

    available:=isAvailableToSteg(mp3File,posmp3old+36,length);
    if ((available) AND (not firsttime)) then
    begin
      if ((posmp3-4)=(posmp3old+36)) then
      begin
        streamHasil.Seek(posmp3-4, soFromBeginning);
        streamHasil.WriteBuffer('XXXX', 4);
        streamHasil.Write(buff1, 1);
        posmp3:=posmp3+1;
      end else begin
        streamHasil.Seek(posmp3, soFromBeginning);
        streamHasil.Write(buff1, 1);
        posmp3:=posmp3+1;
      end;
      n:=n+1;
    end else if ((not available) AND (not firsttime)) then
    begin
      posmp3:=posNext;
    end;

    if ((posmp3>=posNext) AND (not firsttime) AND (posNext<>-1)) then
    begin
      posmp3old:=posNext;
      posNext:=FindNextFrame(resultFile, posmp3old, getMP3Header(resultFile,
          posmp3old));
      posmp3:=posmp3old+40;
    end;
  end;

  streamHasil.Free;
  streamHidden.Free;
  Result:=n;
end;


//function to get hidden file
function RevealFile(mp3File:string): string;
var
  filemp3: File;
  posmp3, posmp3old, n, count, posNext: Integer;
  buff1: byte;
  firsttime:Boolean;
  res: string;
  remaining, len: Integer;
  A: TStringList;
  resultExt: string;
  streamHasil: TFileStream;
begin
  //
  Result:='None';
  firsttime:=True;
  res:='';
  remaining:=255;
  A := TStringList.Create;

  //open mp3 file
  AssignFile(filemp3, mp3File);
  FileMode:=fmOpenRead;
  Reset(filemp3,1);
  posmp3:=FindFirstHeader(mp3File);
  posmp3old:=posmp3;
  posNext:=FindNextFrame(mp3File, posmp3, getMP3Header(mp3File, posmp3));
  seek(filemp3, posmp3);

  //get result file size and extension
  posmp3:=posmp3+40;
  while (firsttime) do
  begin
    if (isStegged(mp3File,posmp3old)) then
    begin
      //get it
      seek(filemp3, posmp3);
      BlockRead(filemp3, buff1, 1, count);
      res:=res+Char(buff1);
      if (buff1=ord('.')) then
      begin
        remaining:=4;
      end;
      remaining:=remaining-1;
      if (remaining<0) then
      begin
        firsttime:=False;
        break;
      end;
      posmp3:=posmp3+1;
    end else begin
      posmp3:=posNext;
    end;

    if (posmp3>=posNext) then
    begin
      posmp3old:=posNext;
      posNext:=FindNextFrame(mp3File, posmp3old, getMP3Header(mp3File,
          posmp3old));
      posmp3:=posmp3old+40;
    end;
  end;

  Split('#', res, A);
  len:=strtoint(A[0]);
  resultExt:=trim(A[1]);

  streamHasil:=TFileStream.Create(mp3File+resultExt, fmCreate or fmShareDenyNone);

  posmp3:=posNext;
  posmp3old:=posmp3;
  posNext:=FindNextFrame(mp3File, posmp3, getMP3Header(mp3File, posmp3));

  n:=0;
  posmp3:=posmp3+40;
  while (n<len) do
  begin
    //
    if (isStegged(mp3File,posmp3old)) then
    begin
      //get it
      seek(filemp3, posmp3);
      BlockRead(filemp3, buff1, 1, count);
      //write it
      streamHasil.Write(buff1,1);
      n:=n+1;
      posmp3:=posmp3+1;
    end else begin
      posmp3:=posNext;
    end;
    
    if (posmp3>=posNext) then
    begin
      posmp3old:=posNext;
      posNext:=FindNextFrame(mp3File, posmp3old, getMP3Header(mp3File,
          posmp3old));
      posmp3:=posmp3old+40;
    end;
  end;

  streamHasil.Free;
  CloseFile(filemp3);
  Result:=mp3File+resultExt;
end;

// return the exact file size for a file. Return zero if the file is not found.
function FileSize(FileName : String) : Int64;
var
  SearchRec : TSearchRec;
begin
  if FindFirst(FileName, faAnyFile, SearchRec ) = 0 then                  // if found
     Result := Int64(SearchRec.FindData.nFileSizeHigh) shl Int64(32) +    // calculate the size
               Int64(SearchREc.FindData.nFileSizeLow)
   else
     Result := 0;
   //FindClose(SearchRec);                                                   // close the find
end;


//split string using specified delimiter
procedure Split(const Delimiter: Char; Input: string; const Strings: TStrings);
begin
   Assert(Assigned(Strings));
   Strings.Clear;
   Strings.Delimiter := Delimiter;
   Strings.DelimitedText := Input;
end;


//pad string (left)
function LeftPad(S: string; Ch: Char; Len: Integer): string;
var
  RestLen: Integer;
begin
  Result  := S;
  RestLen := Len - Length(s);
  if RestLen < 1 then Exit;
  Result := S + StringOfChar(Ch, RestLen);
end;

end.

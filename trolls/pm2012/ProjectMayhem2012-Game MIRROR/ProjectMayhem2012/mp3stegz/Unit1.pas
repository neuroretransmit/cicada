unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, MPlayer, StdCtrls, uMP3, ExtCtrls, DCPcrypt2, DCPrc4, ZLibEx,
  DCPsha1, ComCtrls, Unit2, Unit3, DCPblockciphers, DCPrijndael, jpeg, ShellAPI,
  XPMan;

type
  TfrmMain = class(TForm)
    txtFilename: TEdit;
    btnBrowse: TButton;
    OpenDialog1: TOpenDialog;
    btnFindFirst: TButton;
    txtHiddenFile: TEdit;
    btnBrowseHid: TButton;
    OpenDialog2: TOpenDialog;
    btnHide: TButton;
    txtHiddenLength: TLabeledEdit;
    txtHiddenFileExt: TLabeledEdit;
    txtStegFileResult: TLabeledEdit;
    btnBrowseSteg: TButton;
    OpenDialog3: TOpenDialog;
    btnReveal: TButton;
    txtPassword: TEdit;
    btnCheckSize: TButton;
    btnCheckMaxHidden: TButton;
    DCP_sha11: TDCP_sha1;
    GroupBox1: TGroupBox;
    Memo1: TMemo;
    btnClearMemo: TButton;
    btnAbout: TButton;
    StatusBar1: TStatusBar;
    DCP_rijndael1: TDCP_rijndael;
    Image1: TImage;
    Image2: TImage;
    btnHelp: TButton;
    XPManifest1: TXPManifest;
    Label1: TLabel;
    Label2: TLabel;
    txtPassword2: TEdit;
    procedure btnBrowseClick(Sender: TObject);
    procedure btnFindFirstClick(Sender: TObject);
    procedure btnClearMemoClick(Sender: TObject);
    procedure btnBrowseHidClick(Sender: TObject);
    procedure btnHideClick(Sender: TObject);
    procedure btnBrowseStegClick(Sender: TObject);
    procedure btnRevealClick(Sender: TObject);
    procedure btnCheckMaxHiddenClick(Sender: TObject);
    procedure btnCheckSizeClick(Sender: TObject);
    procedure btnAboutClick(Sender: TObject);
    procedure Image2Click(Sender: TObject);
    procedure Image1Click(Sender: TObject);
    procedure btnHelpClick(Sender: TObject);
  private
    { Private declarations }
    function checkSizeAfter(filename: string; password: string): Integer;
    function encryptAndCompress(filename: string; password: string): Boolean;
    function decompressAndDecrypt(filename: string; password: string): Boolean;
  public
    { Public declarations }
  end;

var
  frmMain: TfrmMain;
  stegFileResult: string;

implementation

{$R *.dfm}

//function to decompress and decrypt
function TfrmMain.decompressAndDecrypt(filename: string; password: string):
Boolean;
var
  SourceCrypt, DestCrypt, InputStream, OutputStream: TFileStream;
  DeCompressionStream: TZDecompressionStream;
begin
  Result:=False;

  //decrypt
  try
    SourceCrypt:= TFileStream.Create(filename, fmOpenRead or fmShareDenyNone);
    DestCrypt:= TFileStream.Create('tmpDecrypt.tmp.zip',fmCreate);
    DCP_rijndael1.InitStr(password,TDCP_sha1);              // initialize the cipher with a hash of the passphrase
    DCP_rijndael1.DecryptStream(SourceCrypt,DestCrypt,SourceCrypt.Size); // decrypt the contents of the file
    DCP_rijndael1.Burn;
    DestCrypt.Free;
    SourceCrypt.Free;
    DeleteFile(filename);
    //Result:=True;
  except
    MessageDlg('File IO error',mtError,[mbOK],0);
  end;

  //decompress
  try
    InputStream := TFileStream.Create('tmpDecrypt.tmp.zip', fmOpenRead or fmShareDenyNone);
    OutputStream := TFileStream.Create(filename, fmCreate);
    DecompressionStream := TZDecompressionStream.Create(InputStream);
    OutputStream.CopyFrom(DecompressionStream, 0);
    DecompressionStream.Free;
    OutputStream.Free;
    InputStream.Free;

    DeleteFile('tmpDecrypt.tmp.zip');
    Result:=True;
  except
    MessageDlg('File IO error',mtError,[mbOK],0);
  end;

end;

//function to encrypt and compress file
function TfrmMain.encryptAndCompress(filename: string; password: string): Boolean;
var
  SourceCrypt, DestCrypt, InputStream, OutputStream: TFileStream;
  CompressionStream: TZCompressionStream;
begin
  Result:=False;
  //compress
  try
    InputStream := TFileStream.Create(filename, fmOpenRead or fmShareDenyNone);
    OutputStream := TFileStream.Create('tmpCrypt.tmp.zip', fmCreate);
    CompressionStream := TZCompressionStream.Create(OutputStream, zcMax);
    CompressionStream.CopyFrom(InputStream, InputStream.Size);
    CompressionStream.Free;
    //Result:=True;
    OutputStream.Free;
    InputStream.Free;
  except
    MessageDlg('File IO error',mtError,[mbOK],0);
  end;

  //crypt
  try
    SourceCrypt:= TFileStream.Create('tmpCrypt.tmp.zip',fmOpenRead or fmShareDenyNone);
    DestCrypt:= TFileStream.Create('tmpCrypt.tmp'+ExtractFileExt(filename),fmCreate);
    DCP_rijndael1.InitStr(password,TDCP_sha1);              // initialize the cipher with a hash of the passphrase
    DCP_rijndael1.EncryptStream(SourceCrypt,DestCrypt,SourceCrypt.Size); // encrypt the contents of the file
    DCP_rijndael1.Burn;
    Result:=True;
    DestCrypt.Free;
    SourceCrypt.Free;
  except
    MessageDlg('File IO error',mtError,[mbOK],0);
  end;

  DeleteFile('tmpCrypt.tmp.zip');
end;

//function to check file size after encryption and compression
function TfrmMain.checkSizeAfter(filename: string; password: string): Integer;
var
  SourceCrypt, DestCrypt, InputStream, OutputStream: TFileStream;
  CompressionStream: TZCompressionStream;
begin
  Result:=-1;
  //compress
  try
    InputStream := TFileStream.Create(filename, fmOpenRead or fmShareDenyNone);
    OutputStream := TFileStream.Create('tmpCrypt.tmp.zip', fmCreate);
    CompressionStream := TZCompressionStream.Create(OutputStream, zcMax);
    CompressionStream.CopyFrom(InputStream, InputStream.Size);
    CompressionStream.Free;
    //Result:=OutputStream.Size;
    OutputStream.Free;
    InputStream.Free;
  except
    MessageDlg('File IO error',mtError,[mbOK],0);
  end;
  //crypt
  try
    SourceCrypt:= TFileStream.Create('tmpCrypt.tmp.zip',fmOpenRead or fmShareDenyNone);
    DestCrypt:= TFileStream.Create('tmpCrypt.tmp',fmCreate);
    DCP_rijndael1.InitStr(password,TDCP_sha1);              // initialize the cipher with a hash of the passphrase
    DCP_rijndael1.EncryptStream(SourceCrypt,DestCrypt,SourceCrypt.Size); // encrypt the contents of the file
    DCP_rijndael1.Burn;
    Result:=DestCrypt.Size;
    DestCrypt.Free;
    SourceCrypt.Free;
  except
    MessageDlg('File IO error',mtError,[mbOK],0);
  end;


  DeleteFile('tmpCrypt.tmp');
  DeleteFile('tmpCrypt.tmp.zip');
end;

procedure TfrmMain.btnBrowseClick(Sender: TObject);
begin
  if (OpenDialog1.Execute) then
  begin
    if FileExists(OpenDialog1.FileName) then
    begin
      txtFilename.Text:=OpenDialog1.FileName;
    end;
  end;
end;

procedure TfrmMain.btnFindFirstClick(Sender: TObject);
var
  pos, posNext: Integer;
  myRawHeader: TRawMP3Header;
  myHeaderArray: TMP3HeaderArray;
begin
  if FileExists(txtFilename.Text) then
  begin
    Memo1.Clear;
    pos:=FindFirstHeader(txtFilename.Text);
    Memo1.Lines.Add('First header found at byte '+inttostr(pos));
    myHeaderArray:=getMP3Header(txtFilename.Text, pos);
    ParseHeaderArray(myHeaderArray, myRawHeader);
    //print result into memo
    Memo1.Lines.Add('Audio version='+inttostr(myRawHeader.AudioVersion));
    Memo1.Lines.Add('Layer index='+inttostr(myRawHeader.LayerIdx));
    Memo1.Lines.Add('Protection bit='+inttostr(myRawHeader.Protection));
    Memo1.Lines.Add('Padding bit='+inttostr(myRawHeader.Padding));
    Memo1.Lines.Add('Frame Size='+inttostr(frameSize(myHeaderArray)));
    posNext:=FindNextFrame(txtFilename.Text, pos, myHeaderArray);
    Memo1.Lines.Add('Frame #2 found at='+inttostr(posNext));
    myHeaderArray:=getMP3Header(txtFilename.Text, posNext);
    Memo1.Lines.Add('Frame Size='+inttostr(frameSize(myHeaderArray)));
    Memo1.Lines.Add('IsVBR='+inttostr(ord(isVBR(txtFilename.text))));
    Memo1.Lines.Add('VBRPos='+inttostr(VBRPos(txtFilename.text)));
    Memo1.Lines.Add('Frame Count='+inttostr(frameCount(txtFilename.text)));
    Memo1.Lines.Add('Frame Available to steg Count='+inttostr(
      FrameAvailableToStegCount(txtFilename.text, 20)));
    Memo1.Lines.Add('Frame Available to steg Bytes='+inttostr(
      MaxStegSize(txtFilename.text, 20)));
  end else
  begin
    MessageDlg('File does not exist!', mtError, [mbOK], 0);
    exit;
  end;
end;

procedure TfrmMain.btnClearMemoClick(Sender: TObject);
begin
  Memo1.Lines.Clear;
end;

procedure TfrmMain.btnBrowseHidClick(Sender: TObject);
begin
  if (OpenDialog2.Execute) then
  begin
    if FileExists(OpenDialog2.FileName) then
    begin
      txtHiddenFile.Text:=OpenDialog2.FileName;
      txtHiddenLength.Text:=inttostr(FileSize(OpenDialog2.FileName));
      txtHiddenFileExt.Text:=ExtractFileExt(OpenDialog2.FileName);
    end;
  end;
end;

procedure TfrmMain.btnHideClick(Sender: TObject);
var
  n: Integer;
begin
  if ((txtPassword.Text='') or (txtPassword2.Text='')) then
  begin
    messageDlg('Please fill the password', mtError, [
      mbOK], 0);
    exit;
  end;

  if (txtPassword.Text<>txtPassword2.Text) then
  begin
    messageDlg('Both password doesn''t match!', mtError, [
      mbOK], 0);
    exit;
  end;

  if (not FileExists(txtFilename.Text)) or (not FileExists(txtHiddenFile.Text)) then
  begin
    messageDlg('Both file (mp3 source and hidden file) must exists', mtError, [
      mbOK], 0);
    exit;
  end;

  stegFileResult:= extractFilePath(txtFilename.Text) +
    extractFileName(txtFilename.Text) + '-steg'+extractFileExt(
      txtFilename.Text);
  txtStegFileResult.Text:=stegFileResult;
  if (encryptAndCompress(txtHiddenFile.Text, txtPassword.Text)) then
  begin
    n:=HideFile(txtFilename.Text, 'tmpCrypt.tmp'+ExtractFileExt(
      txtHiddenFile.Text), stegFileResult, 20);
    if (n>-1) then
    begin
      messageDlg('Hide successful!'+#13+'Result file is '+stegFileResult+#13+'Num. Of Bytes hidden = '+inttostr(n), mtInformation, [mbOK], 0);
    end else begin
      messageDlg('Hide failed!', mtError, [mbOK], 0);
    end;
  end else begin
    messageDlg('Failed to encrypt and compress!', mtError, [mbOK], 0);
  end;

end;

procedure TfrmMain.btnBrowseStegClick(Sender: TObject);
begin
  if (OpenDialog3.Execute) then
  begin
    if FileExists(OpenDialog3.FileName) then
    begin
      txtStegFileResult.Text:=OpenDialog3.FileName;
    end;
  end;
end;

procedure TfrmMain.btnRevealClick(Sender: TObject);
var
  resultName:string;
begin
  if (txtPassword.Text='') then
  begin
    messageDlg('Please fill the password', mtError, [
      mbOK], 0);
    exit;
  end;

  if (not FileExists(txtStegFileResult.Text)) then
  begin
    messageDlg('Stegged-mp3 file does not exist!', mtError, [
      mbOK], 0);
    exit;
  end;

  resultName:=RevealFile(txtStegFileResult.Text);
  if (resultName<>'None') then
  begin
    //success reveal
    //decompress and decrypt
    if (decompressAndDecrypt(resultName, txtPassword.Text)) then
    begin
      messageDlg('Reveal success!'+#13+'Result file is '+resultName, mtInformation, [mbOK], 0);
    end else
    begin
      messageDlg('Reveal failed!', mtError, [mbOK], 0);
    end;
  end else
  begin
    messageDlg('Reveal failed!', mtError, [mbOK], 0);
  end;
end;

procedure TfrmMain.btnCheckMaxHiddenClick(Sender: TObject);
var
  max: Integer;
begin
  if FileExists(txtFilename.Text) then
  begin
    max:=MaxStegSize(txtFilename.Text, 20);
    messageDlg('Maximum file size to hide is '+inttostr(max), mtInformation, [
      mbOK], 0);
    btnCheckMaxHidden.Caption:='Max. Hidden Size='+inttostr(max);
  end else
  begin
    messageDlg('File does not exist ', mtError, [
      mbOK], 0);
  end;
end;

procedure TfrmMain.btnCheckSizeClick(Sender: TObject);
var
  sizeAfter: Integer;
begin
  if (txtPassword.Text='') then
  begin
    messageDlg('Please fill the password', mtError, [
      mbOK], 0);
    exit;
  end;

  if (not FileExists(txtHiddenFile.Text)) then
  begin
    messageDlg('File does not exist ', mtError, [
      mbOK], 0);
    exit;
  end;

  sizeAfter:=checkSizeAfter(txtHiddenFile.Text, txtPassword.Text);
  messageDlg('Size after encryption and compression is '+inttostr(sizeAfter), mtInformation, [
      mbOK], 0);
  btnCheckSize.Caption:='Size after encrypt+compress='+inttostr(sizeAfter);
end;

procedure TfrmMain.btnAboutClick(Sender: TObject);
begin
  AboutBox.ShowModal;
end;

procedure TfrmMain.Image2Click(Sender: TObject);
begin
  ShellExecute(Application.Handle, PChar('open'), PChar('http://achmadz.blogspot.com/'), PChar(0),
    nil, SW_NORMAL);
end;

procedure TfrmMain.Image1Click(Sender: TObject);
begin
  ShellExecute(Application.Handle, PChar('open'), PChar('http://mp3stegz.sourceforge.net/'), PChar(0),
    nil, SW_NORMAL);
end;

procedure TfrmMain.btnHelpClick(Sender: TObject);
begin
//  ShellExecute(Application.Handle, PChar('open'), PChar('HELP.txt'), PChar(0),
//    nil, SW_NORMAL);
  frmHelp.Show;
end;

end.

program mp3stegz;

uses
  Forms,
  Unit1 in 'Unit1.pas' {frmMain},
  uMP3 in 'uMP3.pas',
  Unit2 in 'Unit2.pas' {AboutBox},
  Unit3 in 'Unit3.pas' {frmHelp};

{$R *.res}

begin
  Application.Initialize;
  Application.Title := 'Steganography in MP3 File';
  Application.CreateForm(TfrmMain, frmMain);
  Application.CreateForm(TAboutBox, AboutBox);
  Application.CreateForm(TfrmHelp, frmHelp);
  Application.Run;
end.

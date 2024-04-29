unit Unit2;

interface

uses Windows, SysUtils, Classes, Graphics, Forms, Controls, StdCtrls,
  Buttons, ExtCtrls, ShellAPI, jpeg, XPMan;

type
  TAboutBox = class(TForm)
    Panel1: TPanel;
    ProgramIcon: TImage;
    ProductName: TLabel;
    Version: TLabel;
    Copyright: TLabel;
    Comments: TLabel;
    OKButton: TButton;
    Image1: TImage;
    XPManifest1: TXPManifest;
    procedure Image1Click(Sender: TObject);
    procedure ProgramIconClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  AboutBox: TAboutBox;

implementation

{$R *.dfm}

procedure TAboutBox.Image1Click(Sender: TObject);
begin
  ShellExecute(Application.Handle, PChar('open'), PChar('http://achmadz.blogspot.com/'), PChar(0),
    nil, SW_NORMAL);
end;

procedure TAboutBox.ProgramIconClick(Sender: TObject);
begin
  ShellExecute(Application.Handle, PChar('open'), PChar('http://achmadz.blogspot.com/2008/05/hide-any-file-inside-mp3-file.html'), PChar(0),
    nil, SW_NORMAL);
end;

end.
 

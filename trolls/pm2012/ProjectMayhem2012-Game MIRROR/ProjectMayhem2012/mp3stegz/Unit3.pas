unit Unit3;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, XPMan;

type
  TfrmHelp = class(TForm)
    Memo1: TMemo;
    btnClose: TButton;
    XPManifest1: TXPManifest;
    procedure btnCloseClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmHelp: TfrmHelp;

implementation

{$R *.dfm}

procedure TfrmHelp.btnCloseClick(Sender: TObject);
begin
  Self.Close;
end;

end.

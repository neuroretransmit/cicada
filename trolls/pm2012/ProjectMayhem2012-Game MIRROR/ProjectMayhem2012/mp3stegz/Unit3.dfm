object frmHelp: TfrmHelp
  Left = 324
  Top = 108
  Width = 480
  Height = 436
  BorderIcons = []
  Caption = 'Simple Help for mp3stegz'
  Color = clBtnFace
  Constraints.MinHeight = 436
  Constraints.MinWidth = 480
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  Position = poOwnerFormCenter
  DesignSize = (
    472
    409)
  PixelsPerInch = 96
  TextHeight = 13
  object Memo1: TMemo
    Left = 16
    Top = 24
    Width = 445
    Height = 333
    Anchors = [akLeft, akTop, akRight, akBottom]
    Lines.Strings = (
      '==============To hide a file inside mp3======================'
      '1. Choose '#39'container'#39' mp3 by clicking '#39'Select source mp3'#39' button'
      
        '- You may check maximum hidden data size that previously selecte' +
        'd mp3 can handle '
      'by clicking '#39'Max. Hidden Size'#39
      '- You may check selected mp3 info by clicking '#39'Get mp3 info'#39
      
        '2. Choose a file you want to hide by clicking '#39'Select Hidden Fil' +
        'e'#39
      
        '- You may check file size after encryption and compression by cl' +
        'icking '#39'Size after '
      'encrypt+compress'#39
      
        '3. Type your password in the provided textbox. Do not forget thi' +
        's password since this '
      'application have no input for confirmation password.'
      
        '4. Click '#39'Hide It!'#39' to begin hiding data. Please be patient sinc' +
        'e the algorithm is not '
      'optimized, so, the application maybe look not responding.'
      
        '5. For example, if your source mp3 is '#39'one.mp3'#39', the stegged-mp3' +
        ' result will have file '
      'name '#39'one.mp3-steg.mp3'#39' located in the same folder as '#39'one.mp3'#39
      ''
      '==============To reveal/get hidden file inside mp3==========='
      
        '1. type your password in the textbox provided. Wrong password wi' +
        'll cause damaged '
      'result file.'
      '2. Choose stegged-mp3 file by clicking '#39'Select Stegged-mp3'#39'.'
      '3. Click '#39'Reveal!'#39' to begin revealing hidden file.'
      
        '4. For example, if your stegged-mp3 file is '#39'one.mp3-steg.mp3'#39' a' +
        'nd you hidden data is '
      
        #39'.jpg'#39' file, result file will have file name '#39'one.mp3-steg.mp3.j' +
        'pg'#39' located in the same '
      'folder as '#39'one.mp3-steg.mp3'#39'.')
    ScrollBars = ssBoth
    TabOrder = 0
  end
  object btnClose: TButton
    Left = 192
    Top = 372
    Width = 73
    Height = 25
    Anchors = [akLeft, akRight, akBottom]
    Caption = 'Close'
    TabOrder = 1
    OnClick = btnCloseClick
  end
  object XPManifest1: TXPManifest
    Left = 280
    Top = 368
  end
end

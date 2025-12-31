[Setup]
AppId={{C7F9A8B3-2F91-4D3A-9A45-CLICKER0001}}
AppName=ClicKer
AppVersion=1.0.0
AppPublisher=Korvuz
AppPublisherURL=https://github.com/K0rvuz
AppSupportURL=https://github.com/K0rvuz
AppUpdatesURL=https://github.com/K0rvuz
DefaultDirName={localappdata}\Programs\ClicKer
DefaultGroupName=ClicKer
OutputBaseFilename=ClicKerInstaller
SetupIconFile="C:\Users\colov\Desktop\ClicKer\assets\clicker.ico"
UninstallDisplayIcon={app}\ClicKer.exe
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
WizardStyle=modern

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "ClicKer.dist\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
; Atalho na área de trabalho do usuário atual
Name: "{userdesktop}\ClicKer"; Filename: "{app}\ClicKer.exe"
; Atalho no menu iniciar do usuário atual
Name: "{group}\ClicKer"; Filename: "{app}\ClicKer.exe"

[Run]
Filename: "{app}\ClicKer.exe"; Description: "Abrir ClicKer"; Flags: nowait postinstall skipifsilent

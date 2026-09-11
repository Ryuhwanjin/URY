; URY Windows installer (v0.9.6)
; The installer owns only the application directory. User data remains in %USERPROFILE%\Desktop\URY.

#define MyAppName "URY"
#define MyAppVersion "0.9.6"
#define MyAppPublisher "Ryu.H.J"

[Setup]
AppId=URY
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\URY
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
CloseApplications=yes
OutputDir=..\dist\installer
OutputBaseFilename=URY_Setup_v{#MyAppVersion}
SetupIconFile=..\URY_Windows\app_icon.ico
UninstallDisplayIcon={app}\URY.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "..\dist\URY\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\URY.exe"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\URY.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\URY.exe"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

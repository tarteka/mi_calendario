#define MyAppName "Generador Calendario"
#define MyAppVersion GetEnv("APP_VERSION")
#define MyAppExeName "Generador_Calendario.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={pf}\GeneradorCalendario
DefaultGroupName={#MyAppName}
OutputDir=..\dist
OutputBaseFilename=Generador_Calendario_{#MyAppVersion}
Compression=lzma
SolidCompression=yes
SetupIconFile=..\assets\icon.ico

[Files]
Source: "..\dist\Generador_Calendario\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir aplicación"; Flags: nowait postinstall skipifsilent

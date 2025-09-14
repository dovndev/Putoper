
[Setup]
AppName=Auto Typer
AppVersion=1.0
DefaultDirName={autopf}\AutoTyper
DefaultGroupName=Auto Typer
OutputDir=installer_output
OutputBaseFilename=AutoTyper_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\AutoTyper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Auto Typer"; Filename: "{app}\AutoTyper.exe"
Name: "{autodesktop}\Auto Typer"; Filename: "{app}\AutoTyper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AutoTyper.exe"; Description: "{cm:LaunchProgram,Auto Typer}"; Flags: nowait postinstall skipifsilent

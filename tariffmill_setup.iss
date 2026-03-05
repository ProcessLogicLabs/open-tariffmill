; Inno Setup Script for TariffMill
; Build with: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" tariffmill_setup.iss

#define MyAppName "TariffMill"
#define MyAppVersion "0.98.1"
#define MyAppPublisher "TariffMill"
#define MyAppExeName "TariffMill.exe"
#define SourceDir "dist\TariffMill"
; IMPORTANT: Replace this placeholder with your actual GitHub token before building
; Or pass via command line: ISCC.exe /dGitHubToken=your_token_here tariffmill_setup.iss
#ifndef GitHubToken
  #define GitHubToken "YOUR_GITHUB_TOKEN_HERE"
#endif

[Setup]
; Application info
AppId={{8F3B9A2E-5C7D-4E1F-B8A6-9D2C3E4F5A6B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=TariffMill_Setup_{#MyAppVersion}
SetupIconFile=Tariffmill\Resources\icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

; Privileges - install to user's local appdata (no admin required)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Uninstall info
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; All files from the PyInstaller dist folder
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Bundle auth_users.json (required for fresh installs to avoid hang)
Source: "auth_users.json"; DestDir: "{app}"; Flags: ignoreversion confirmoverwrite

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\Resources\icon.ico"; WorkingDir: "{app}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\Resources\icon.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Registry]
; DISABLED: Setting env var during install can cause hangs on fresh installs
; Users can set TARIFFMILL_GITHUB_TOKEN manually if needed for remote updates
; For now, we bundle auth_users.json directly with the installer
;Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName: "TARIFFMILL_GITHUB_TOKEN"; ValueData: "{#GitHubToken}"; Flags: uninsdeletevalue

[Run]
; Launch application after installation (now safe with Windows auto-login enabled)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runasoriginaluser shellexec

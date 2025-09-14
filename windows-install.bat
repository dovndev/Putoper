@echo off
REM Windows Installer Script for Auto Typer
REM This creates a proper Windows installation

setlocal EnableDelayedExpansion

set "APP_NAME=Auto Typer"
set "VERSION=1.0.0"
set "INSTALL_DIR=%ProgramFiles%\Auto Typer"
set "START_MENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs"
set "DESKTOP=%PUBLIC%\Desktop"

echo.
echo ================================
echo    Auto Typer Windows Installer
echo ================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges
) else (
    echo [ERROR] This installer requires administrator privileges
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Check if executable exists
if not exist "dist\AutoTyper.exe" (
    echo [ERROR] AutoTyper.exe not found in dist directory
    echo Please run the build script first
    pause
    exit /b 1
)

echo [INFO] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [INFO] Copying application files...
copy "dist\AutoTyper.exe" "%INSTALL_DIR%\" >nul
if %errorLevel% neq 0 (
    echo [ERROR] Failed to copy AutoTyper.exe
    pause
    exit /b 1
)

REM Create uninstaller
echo [INFO] Creating uninstaller...
(
echo @echo off
echo echo Uninstalling Auto Typer...
echo rmdir /s /q "%INSTALL_DIR%"
echo del "%START_MENU%\Auto Typer.lnk" 2^>nul
echo del "%DESKTOP%\Auto Typer.lnk" 2^>nul
echo reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /f 2^>nul
echo echo Auto Typer has been uninstalled.
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

echo [INFO] Creating Start Menu shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\Auto Typer.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\AutoTyper.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Modern Text Automation Tool'; $Shortcut.Save()"

echo [INFO] Creating Desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Auto Typer.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\AutoTyper.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Modern Text Automation Tool'; $Shortcut.Save()"

echo [INFO] Adding to Windows Registry...
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /v "DisplayName" /t REG_SZ /d "Auto Typer" /f >nul
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /v "DisplayVersion" /t REG_SZ /d "%VERSION%" /f >nul
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /v "Publisher" /t REG_SZ /d "Auto Typer Team" /f >nul
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyper" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\AutoTyper.exe" /f >nul

echo.
echo ================================
echo    Installation Complete!
echo ================================
echo.
echo Auto Typer has been installed successfully.
echo.
echo You can now:
echo   • Find "Auto Typer" in the Start Menu
echo   • Use the Desktop shortcut
echo   • Run from: %INSTALL_DIR%\AutoTyper.exe
echo.
echo To uninstall, use Windows Add/Remove Programs
echo or run: %INSTALL_DIR%\uninstall.bat
echo.
pause

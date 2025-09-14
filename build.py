#!/usr/bin/env python3
"""
Build Script for Auto Typer
Creates distributable packages for Windows and Linux
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

class AutoTyperBuilder:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.installer_dir = self.project_dir / "installers"
        
    def clean(self):
        """Clean previous builds"""
        print("🧹 Cleaning previous builds...")
        for dir_path in [self.dist_dir, self.build_dir, self.installer_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
        print("✅ Clean complete")
        
    def create_executable(self):
        """Create executable using PyInstaller"""
        print("🔨 Creating executable...")
        
        # Create PyInstaller spec
        spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['auto_typing.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['customtkinter', 'darkdetect', 'packaging'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoTyper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
        
        with open(self.project_dir / "auto_typer.spec", "w") as f:
            f.write(spec_content)
            
        # Run PyInstaller
        try:
            subprocess.run([
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "auto_typer.spec"
            ], check=True, cwd=self.project_dir)
            print("✅ Executable created successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create executable: {e}")
            return False
        return True
        
    def create_windows_installer(self):
        """Create Windows installer using NSIS"""
        if platform.system() != "Windows":
            print("⚠️ Windows installer can only be built on Windows")
            return False
            
        print("🪟 Creating Windows installer...")
        
        # Create NSIS script
        nsis_script = f'''
!define APPNAME "Auto Typer"
!define COMPANYNAME "Auto Typer Team"
!define DESCRIPTION "Modern Text Automation Tool"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/yourrepo/auto-typer"
!define UPDATEURL "https://github.com/yourrepo/auto-typer"
!define ABOUTURL "https://github.com/yourrepo/auto-typer"
!define INSTALLSIZE 50000

RequestExecutionLevel admin

InstallDir "$PROGRAMFILES\\${{APPNAME}}"

Name "${{APPNAME}}"
OutFile "installers\\AutoTyper-Setup.exe"

Page directory
Page instfiles

Section "install"
    SetOutPath "$INSTDIR"
    File "dist\\AutoTyper.exe"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\\${{APPNAME}}"
    CreateShortcut "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk" "$INSTDIR\\AutoTyper.exe"
    CreateShortcut "$SMPROGRAMS\\${{APPNAME}}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    CreateShortcut "$DESKTOP\\${{APPNAME}}.lnk" "$INSTDIR\\AutoTyper.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayName" "${{APPNAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "HelpLink" "${{HELPURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "URLUpdateInfo" "${{UPDATEURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "URLInfoAbout" "${{ABOUTURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "EstimatedSize" ${{INSTALLSIZE}}
SectionEnd

Section "uninstall"
    Delete "$INSTDIR\\AutoTyper.exe"
    Delete "$INSTDIR\\uninstall.exe"
    
    Delete "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk"
    Delete "$SMPROGRAMS\\${{APPNAME}}\\Uninstall.lnk"
    RMDir "$SMPROGRAMS\\${{APPNAME}}"
    Delete "$DESKTOP\\${{APPNAME}}.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}"
    
    RMDir "$INSTDIR"
SectionEnd
'''
        
        self.installer_dir.mkdir(exist_ok=True)
        nsis_file = self.project_dir / "installer.nsi"
        
        with open(nsis_file, "w") as f:
            f.write(nsis_script)
            
        try:
            subprocess.run(["makensis", str(nsis_file)], check=True)
            print("✅ Windows installer created successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ NSIS not found. Please install NSIS to create Windows installer")
            return False
            
    def create_linux_deb(self):
        """Create Debian package for Linux"""
        print("🐧 Creating Linux .deb package...")
        
        # Create package structure
        pkg_dir = self.build_dir / "auto-typer-deb"
        debian_dir = pkg_dir / "DEBIAN"
        usr_dir = pkg_dir / "usr"
        bin_dir = usr_dir / "bin"
        apps_dir = usr_dir / "share" / "applications"
        
        for dir_path in [debian_dir, bin_dir, apps_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Copy executable
        shutil.copy2(self.dist_dir / "AutoTyper", bin_dir / "auto-typer")
        os.chmod(bin_dir / "auto-typer", 0o755)
        
        # Create control file
        control_content = '''Package: auto-typer
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Depends: libc6, libx11-6, libxtst6
Maintainer: Auto Typer Team <team@autotyper.com>
Description: Modern Text Automation Tool
 A cross-platform application for automated text typing
 with a modern user interface built with CustomTkinter.
'''
        
        with open(debian_dir / "control", "w") as f:
            f.write(control_content)
            
        # Create desktop file
        desktop_content = '''[Desktop Entry]
Name=Auto Typer
Comment=Modern Text Automation Tool
Exec=auto-typer
Icon=auto-typer
Terminal=false
Type=Application
Categories=Utility;
StartupWMClass=auto-typer
'''
        
        with open(apps_dir / "auto-typer.desktop", "w") as f:
            f.write(desktop_content)
            
        # Build package
        self.installer_dir.mkdir(exist_ok=True)
        deb_file = self.installer_dir / "auto-typer_1.0.0_amd64.deb"
        
        try:
            subprocess.run([
                "dpkg-deb", "--build", str(pkg_dir), str(deb_file)
            ], check=True)
            print("✅ Linux .deb package created successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ dpkg-deb not found. Please install dpkg-dev to create .deb packages")
            return False
            
    def create_appimage(self):
        """Create AppImage for universal Linux compatibility"""
        print("📦 Creating AppImage...")
        
        # Create AppDir structure
        appdir = self.build_dir / "AutoTyper.AppDir"
        usr_dir = appdir / "usr"
        bin_dir = usr_dir / "bin"
        
        for dir_path in [bin_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Copy executable
        shutil.copy2(self.dist_dir / "AutoTyper", bin_dir / "AutoTyper")
        os.chmod(bin_dir / "AutoTyper", 0o755)
        
        # Create AppRun
        apprun_content = '''#!/bin/bash
cd "$(dirname "$0")"
exec ./usr/bin/AutoTyper "$@"
'''
        
        with open(appdir / "AppRun", "w") as f:
            f.write(apprun_content)
        os.chmod(appdir / "AppRun", 0o755)
        
        # Create desktop file
        desktop_content = '''[Desktop Entry]
Name=Auto Typer
Exec=AutoTyper
Icon=auto-typer
Type=Application
Categories=Utility;
'''
        
        with open(appdir / "auto-typer.desktop", "w") as f:
            f.write(desktop_content)
            
        # Try to create AppImage
        try:
            # Download appimagetool if not exists
            appimagetool = self.project_dir / "appimagetool"
            if not appimagetool.exists():
                subprocess.run([
                    "wget", "-O", str(appimagetool),
                    "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
                ], check=True)
                os.chmod(appimagetool, 0o755)
                
            self.installer_dir.mkdir(exist_ok=True)
            subprocess.run([
                str(appimagetool), str(appdir),
                str(self.installer_dir / "AutoTyper-x86_64.AppImage")
            ], check=True)
            print("✅ AppImage created successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Failed to create AppImage")
            return False
            
    def create_portable_archive(self):
        """Create portable archive for all platforms"""
        print("📦 Creating portable archive...")
        
        self.installer_dir.mkdir(exist_ok=True)
        
        # Create portable directory
        portable_dir = self.build_dir / "AutoTyper-Portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copy executable
        if platform.system() == "Windows":
            shutil.copy2(self.dist_dir / "AutoTyper.exe", portable_dir)
            archive_name = "AutoTyper-Portable-Windows.zip"
        else:
            shutil.copy2(self.dist_dir / "AutoTyper", portable_dir)
            os.chmod(portable_dir / "AutoTyper", 0o755)
            archive_name = "AutoTyper-Portable-Linux.tar.gz"
            
        # Create README
        readme_content = '''Auto Typer - Portable Version

To run Auto Typer:
- Windows: Double-click AutoTyper.exe
- Linux: Run ./AutoTyper in terminal or double-click

This is a portable version that doesn't require installation.
Just extract and run!

For more information, visit: https://github.com/yourrepo/auto-typer
'''
        
        with open(portable_dir / "README.txt", "w") as f:
            f.write(readme_content)
            
        # Create archive
        archive_path = self.installer_dir / archive_name
        
        if platform.system() == "Windows":
            shutil.make_archive(
                str(archive_path).replace('.zip', ''),
                'zip',
                str(self.build_dir),
                'AutoTyper-Portable'
            )
        else:
            shutil.make_archive(
                str(archive_path).replace('.tar.gz', ''),
                'gztar',
                str(self.build_dir),
                'AutoTyper-Portable'
            )
            
        print("✅ Portable archive created successfully")
        return True
        
    def build_all(self):
        """Build all packages"""
        print("🚀 Starting Auto Typer build process...")
        
        # Clean previous builds
        self.clean()
        
        # Create executable
        if not self.create_executable():
            print("❌ Build failed at executable creation")
            return False
            
        # Create platform-specific installers
        success = False
        
        if platform.system() == "Windows":
            success = self.create_windows_installer()
        else:
            # Linux
            deb_success = self.create_linux_deb()
            appimage_success = self.create_appimage()
            success = deb_success or appimage_success
            
        # Create portable archive
        self.create_portable_archive()
        
        # Summary
        print("\n" + "="*50)
        print("🎉 Build Summary:")
        print("="*50)
        
        if self.installer_dir.exists():
            for file in self.installer_dir.iterdir():
                print(f"✅ {file.name}")
        else:
            print("❌ No installers created")
            
        print("\nBuild complete! Check the 'installers' directory.")
        return success

def main():
    """Main entry point"""
    builder = AutoTyperBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clean":
            builder.clean()
        elif command == "exe":
            builder.create_executable()
        elif command == "windows":
            builder.create_windows_installer()
        elif command == "linux":
            builder.create_linux_deb()
            builder.create_appimage()
        elif command == "portable":
            builder.create_portable_archive()
        else:
            print("Usage: python build.py [clean|exe|windows|linux|portable]")
    else:
        builder.build_all()

if __name__ == "__main__":
    main()

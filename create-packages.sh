#!/bin/bash
# Cross-platform package creator for Auto Typer

set -e

VERSION="1.0.0"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_DIR="$PROJECT_DIR/packages"

echo "🚀 Creating Auto Typer distribution packages..."

# Clean and create packages directory
rm -rf "$PACKAGES_DIR"
mkdir -p "$PACKAGES_DIR"

# Build executable first
echo "🔨 Building executable..."
cd "$PROJECT_DIR"
python build.py exe

if [ ! -f "dist/AutoTyper" ]; then
    echo "❌ Failed to build executable"
    exit 1
fi

# Create Linux package
echo "📦 Creating Linux package..."
LINUX_PKG="$PACKAGES_DIR/auto-typer-linux-v$VERSION"
mkdir -p "$LINUX_PKG"

# Copy files to Linux package
cp dist/AutoTyper "$LINUX_PKG/"
cp universal-install.sh "$LINUX_PKG/install.sh"
cp README.md "$LINUX_PKG/"
cp requirements.txt "$LINUX_PKG/"
cp auto_typing.py "$LINUX_PKG/"

# Create Linux package README
cat > "$LINUX_PKG/INSTALL.txt" << EOF
Auto Typer v$VERSION - Linux Installation
=========================================

Quick Install:
--------------
1. Run: ./install.sh
2. Follow the prompts

Manual Install:
---------------
1. Copy AutoTyper to desired location
2. Make executable: chmod +x AutoTyper
3. Run: ./AutoTyper

From Source:
------------
1. Install Python 3.8+
2. Run: pip install -r requirements.txt
3. Run: python auto_typing.py

For more information, see README.md
EOF

# Create Linux archive
cd "$PACKAGES_DIR"
tar -czf "auto-typer-linux-v$VERSION.tar.gz" "auto-typer-linux-v$VERSION"
echo "✅ Linux package: auto-typer-linux-v$VERSION.tar.gz"

# Create Windows package (cross-compile)
echo "📦 Creating Windows package..."
cd "$PROJECT_DIR"

# Create Windows spec for PyInstaller
cat > windows_build.spec << 'EOF'
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
EOF

# Try to build Windows executable (may not work on Linux)
echo "🪟 Attempting Windows build..."
python -m PyInstaller --clean windows_build.spec 2>/dev/null || echo "⚠️ Windows build failed (expected on Linux)"

# Create Windows package structure anyway
WINDOWS_PKG="$PACKAGES_DIR/auto-typer-windows-v$VERSION"
mkdir -p "$WINDOWS_PKG"

# Copy available files
if [ -f "dist/AutoTyper.exe" ]; then
    cp dist/AutoTyper.exe "$WINDOWS_PKG/"
else
    echo "⚠️ No Windows executable available. Package will contain source only."
fi

cp windows-install.bat "$WINDOWS_PKG/"
cp README.md "$WINDOWS_PKG/"
cp requirements.txt "$WINDOWS_PKG/"
cp auto_typing.py "$WINDOWS_PKG/"

# Create Windows README
cat > "$WINDOWS_PKG/INSTALL.txt" << EOF
Auto Typer v$VERSION - Windows Installation
===========================================

If AutoTyper.exe is available:
------------------------------
1. Right-click windows-install.bat
2. Select "Run as administrator"
3. Follow the installation prompts

OR simply run AutoTyper.exe directly (portable mode)

From Source (if no .exe):
-------------------------
1. Install Python 3.8+ from python.org
2. Open Command Prompt
3. Run: pip install -r requirements.txt
4. Run: python auto_typing.py

For more information, see README.md
EOF

# Create Windows archive
cd "$PACKAGES_DIR"
if command -v zip >/dev/null 2>&1; then
    zip -r "auto-typer-windows-v$VERSION.zip" "auto-typer-windows-v$VERSION/" >/dev/null
    echo "✅ Windows package: auto-typer-windows-v$VERSION.zip"
else
    tar -czf "auto-typer-windows-v$VERSION.tar.gz" "auto-typer-windows-v$VERSION"
    echo "✅ Windows package: auto-typer-windows-v$VERSION.tar.gz"
fi

# Create universal source package
echo "📦 Creating universal source package..."
UNIVERSAL_PKG="$PACKAGES_DIR/auto-typer-source-v$VERSION"
mkdir -p "$UNIVERSAL_PKG"

cd "$PROJECT_DIR"
cp auto_typing.py "$UNIVERSAL_PKG/"
cp requirements.txt "$UNIVERSAL_PKG/"
cp README.md "$UNIVERSAL_PKG/"
cp setup.sh "$UNIVERSAL_PKG/" 2>/dev/null || true
cp build.py "$UNIVERSAL_PKG/"
cp universal-install.sh "$UNIVERSAL_PKG/install.sh"
cp windows-install.bat "$UNIVERSAL_PKG/"

# Create universal README
cat > "$UNIVERSAL_PKG/INSTALL.txt" << EOF
Auto Typer v$VERSION - Universal Source Package
===============================================

This package contains the source code and can be run on any platform.

Requirements:
-------------
- Python 3.8 or higher
- pip (Python package installer)

Installation:
-------------
1. Extract this package
2. Open terminal/command prompt in the extracted folder
3. Run: pip install -r requirements.txt
4. Run: python auto_typing.py

Platform-specific installation:
-------------------------------
- Linux: Run ./install.sh (after building)
- Windows: Run windows-install.bat as administrator (after building)

Building executables:
--------------------
1. Install PyInstaller: pip install pyinstaller
2. Run: python build.py

For more information, see README.md
EOF

cd "$PACKAGES_DIR"
tar -czf "auto-typer-source-v$VERSION.tar.gz" "auto-typer-source-v$VERSION"
echo "✅ Universal source package: auto-typer-source-v$VERSION.tar.gz"

# Create release info
cat > "RELEASE-INFO.txt" << EOF
Auto Typer v$VERSION - Release Packages
=======================================

Available packages:

1. auto-typer-linux-v$VERSION.tar.gz
   - Linux executable + installer
   - Ready to install and run
   - Recommended for Linux users

2. auto-typer-windows-v$VERSION.{zip,tar.gz}
   - Windows executable + installer (if available)
   - Run windows-install.bat as administrator
   - Recommended for Windows users

3. auto-typer-source-v$VERSION.tar.gz
   - Universal source code package
   - Works on any platform with Python
   - For developers and advanced users

Installation Instructions:
-------------------------

Linux:
  1. Extract: tar -xzf auto-typer-linux-v$VERSION.tar.gz
  2. Enter directory: cd auto-typer-linux-v$VERSION
  3. Install: ./install.sh

Windows:
  1. Extract the Windows package
  2. Right-click windows-install.bat
  3. Select "Run as administrator"

Source (Any platform):
  1. Extract: tar -xzf auto-typer-source-v$VERSION.tar.gz
  2. Enter directory: cd auto-typer-source-v$VERSION
  3. Install: pip install -r requirements.txt
  4. Run: python auto_typing.py

Requirements:
------------
- Python 3.8+ (for source installation)
- Linux: X11 display server
- Windows: Windows 7+

Support:
--------
For issues and questions, see README.md in any package.
EOF

# Summary
echo ""
echo "🎉 Package creation complete!"
echo ""
echo "Created packages:"
cd "$PACKAGES_DIR"
ls -la *.{tar.gz,zip} 2>/dev/null || ls -la *.tar.gz
echo ""
echo "📄 Release info: $PACKAGES_DIR/RELEASE-INFO.txt"
echo "📁 All packages are in: $PACKAGES_DIR"

# Cleanup
cd "$PROJECT_DIR"
rm -f windows_build.spec

echo ""
echo "✅ Ready for distribution!"

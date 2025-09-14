#!/bin/bash
# Install script for Auto Typer on Linux

set -e

INSTALL_DIR="/opt/auto-typer"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/pixmaps"

echo "🚀 Installing Auto Typer..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as root"
    exit 1
fi

# Check if sudo is available
if ! command -v sudo &> /dev/null; then
    echo "❌ sudo is required for installation"
    exit 1
fi

# Create installation directory
echo "📁 Creating installation directory..."
sudo mkdir -p "$INSTALL_DIR"

# Copy executable
echo "📋 Copying executable..."
if [ -f "dist/AutoTyper" ]; then
    sudo cp "dist/AutoTyper" "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/AutoTyper"
else
    echo "❌ AutoTyper executable not found. Please run 'python build.py' first."
    exit 1
fi

# Create launcher script
echo "🔗 Creating launcher script..."
sudo tee "$BIN_DIR/auto-typer" > /dev/null << EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec ./AutoTyper "\$@"
EOF
sudo chmod +x "$BIN_DIR/auto-typer"

# Create desktop entry
echo "🖥️ Creating desktop entry..."
sudo tee "$DESKTOP_DIR/auto-typer.desktop" > /dev/null << EOF
[Desktop Entry]
Name=Auto Typer
Comment=Modern Text Automation Tool
Exec=auto-typer
Icon=auto-typer
Terminal=false
Type=Application
Categories=Utility;Productivity;
Keywords=typing;automation;text;
StartupWMClass=Auto Typer
EOF

# Create simple icon (text-based)
echo "🎨 Creating icon..."
sudo tee "$ICON_DIR/auto-typer.xpm" > /dev/null << 'EOF'
/* XPM */
static char * auto_typer_xpm[] = {
"32 32 3 1",
" 	c None",
".	c #000000",
"+	c #FFFFFF",
"                                ",
"  ..........................    ",
"  .++++++++++++++++++++++++.    ",
"  .++++++++++++++++++++++++.    ",
"  .++....................++.    ",
"  .++.                  .++.    ",
"  .++.   AUTO TYPER     .++.    ",
"  .++.                  .++.    ",
"  .++.  [Text Input]    .++.    ",
"  .++.  ____________    .++.    ",
"  .++. |            |   .++.    ",
"  .++. |            |   .++.    ",
"  .++. |____________|   .++.    ",
"  .++.                  .++.    ",
"  .++.    [Start]       .++.    ",
"  .++.                  .++.    ",
"  .++....................++.    ",
"  .++++++++++++++++++++++++.    ",
"  .++++++++++++++++++++++++.    ",
"  ..........................    ",
"                                ",
"                                "
};
EOF

# Update desktop database
echo "🔄 Updating desktop database..."
if command -v update-desktop-database &> /dev/null; then
    sudo update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo ""
echo "✅ Auto Typer installed successfully!"
echo ""
echo "You can now:"
echo "  • Run 'auto-typer' from the command line"
echo "  • Find 'Auto Typer' in your applications menu"
echo "  • Launch it from the desktop"
echo ""
echo "To uninstall, run: sudo rm -rf '$INSTALL_DIR' '$BIN_DIR/auto-typer' '$DESKTOP_DIR/auto-typer.desktop' '$ICON_DIR/auto-typer.xpm'"

#!/bin/bash
# Universal installer for Auto Typer
# Works on most Linux distributions

set -e

APP_NAME="Auto Typer"
APP_EXEC="auto-typer"
VERSION="1.0.0"
INSTALL_DIR="/opt/auto-typer"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
USER_DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="/usr/share/pixmaps"
USER_ICON_DIR="$HOME/.local/share/icons"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. Installing system-wide."
        SYSTEM_INSTALL=true
    else
        print_status "Running as regular user. Will attempt user installation."
        SYSTEM_INSTALL=false
    fi
}

# Create necessary directories
create_directories() {
    if [ "$SYSTEM_INSTALL" = true ]; then
        mkdir -p "$INSTALL_DIR" "$DESKTOP_DIR" "$ICON_DIR"
    else
        # User installation
        INSTALL_DIR="$HOME/.local/opt/auto-typer"
        BIN_DIR="$HOME/.local/bin"
        mkdir -p "$INSTALL_DIR" "$USER_DESKTOP_DIR" "$USER_ICON_DIR" "$BIN_DIR"
        DESKTOP_DIR="$USER_DESKTOP_DIR"
        ICON_DIR="$USER_ICON_DIR"
    fi
}

# Install executable
install_executable() {
    print_status "Installing executable..."
    
    if [ -f "dist/AutoTyper" ]; then
        cp "dist/AutoTyper" "$INSTALL_DIR/"
        chmod +x "$INSTALL_DIR/AutoTyper"
    else
        print_error "AutoTyper executable not found. Please run 'python build.py exe' first."
        exit 1
    fi
    
    # Create launcher script
    cat > "$BIN_DIR/$APP_EXEC" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec ./AutoTyper "\$@"
EOF
    chmod +x "$BIN_DIR/$APP_EXEC"
    
    print_success "Executable installed to $INSTALL_DIR"
}

# Create desktop entry
create_desktop_entry() {
    print_status "Creating desktop entry..."
    
    cat > "$DESKTOP_DIR/auto-typer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Modern Text Automation Tool
Exec=$APP_EXEC
Icon=auto-typer
Terminal=false
Categories=Utility;Productivity;Office;
Keywords=typing;automation;text;productivity;
StartupWMClass=Auto Typer
MimeType=text/plain;
EOF
    
    chmod +x "$DESKTOP_DIR/auto-typer.desktop"
    print_success "Desktop entry created"
}

# Create icon
create_icon() {
    print_status "Creating application icon..."
    
    # Create a simple SVG icon
    cat > "$ICON_DIR/auto-typer.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="8" fill="#2563eb"/>
  <rect x="8" y="12" width="48" height="40" rx="4" fill="#ffffff"/>
  <rect x="12" y="16" width="40" height="2" fill="#6b7280"/>
  <rect x="12" y="20" width="32" fill="#6b7280" height="2"/>
  <rect x="12" y="24" width="36" height="2" fill="#6b7280"/>
  <rect x="12" y="28" width="28" height="2" fill="#6b7280"/>
  <rect x="12" y="32" width="35" height="2" fill="#2563eb"/>
  <rect x="12" y="36" width="25" height="2" fill="#6b7280"/>
  <rect x="12" y="40" width="30" height="2" fill="#6b7280"/>
  <circle cx="48" cy="48" r="6" fill="#10b981"/>
  <path d="M45 48l2 2 4-4" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
EOF
    
    print_success "Icon created"
}

# Update desktop database
update_desktop_database() {
    print_status "Updating desktop database..."
    
    if command -v update-desktop-database &> /dev/null; then
        if [ "$SYSTEM_INSTALL" = true ]; then
            update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
        else
            update-desktop-database "$USER_DESKTOP_DIR" 2>/dev/null || true
        fi
        print_success "Desktop database updated"
    else
        print_warning "update-desktop-database not found, skipping"
    fi
}

# Add to PATH if needed
update_path() {
    if [ "$SYSTEM_INSTALL" = false ]; then
        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            print_status "Adding ~/.local/bin to PATH..."
            
            # Add to .bashrc if it exists
            if [ -f "$HOME/.bashrc" ]; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
                print_success "Added to ~/.bashrc"
            fi
            
            # Add to .profile if it exists
            if [ -f "$HOME/.profile" ]; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
                print_success "Added to ~/.profile"
            fi
            
            print_warning "Please restart your terminal or run 'source ~/.bashrc' to use the 'auto-typer' command"
        fi
    fi
}

# Uninstall function
uninstall() {
    print_status "Uninstalling Auto Typer..."
    
    if [ "$SYSTEM_INSTALL" = true ]; then
        rm -rf "$INSTALL_DIR"
        rm -f "$BIN_DIR/$APP_EXEC"
        rm -f "$DESKTOP_DIR/auto-typer.desktop"
        rm -f "$ICON_DIR/auto-typer.svg"
    else
        INSTALL_DIR="$HOME/.local/opt/auto-typer"
        BIN_DIR="$HOME/.local/bin"
        rm -rf "$INSTALL_DIR"
        rm -f "$BIN_DIR/$APP_EXEC"
        rm -f "$USER_DESKTOP_DIR/auto-typer.desktop"
        rm -f "$USER_ICON_DIR/auto-typer.svg"
    fi
    
    update_desktop_database
    print_success "Auto Typer uninstalled successfully"
}

# Main installation function
install() {
    print_status "🚀 Installing $APP_NAME v$VERSION..."
    echo
    
    check_root
    create_directories
    install_executable
    create_desktop_entry
    create_icon
    update_desktop_database
    update_path
    
    echo
    print_success "✅ Installation completed successfully!"
    echo
    echo "You can now:"
    if [ "$SYSTEM_INSTALL" = true ]; then
        echo "  • Run 'auto-typer' from the command line"
    else
        echo "  • Run 'auto-typer' from the command line (restart terminal first)"
    fi
    echo "  • Find '$APP_NAME' in your applications menu"
    echo "  • Launch it from the desktop"
    echo
    echo "To uninstall, run: $0 --uninstall"
}

# Help function
show_help() {
    echo "Auto Typer Installer v$VERSION"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --install     Install Auto Typer (default)"
    echo "  --uninstall   Uninstall Auto Typer"
    echo "  --help        Show this help message"
    echo
    echo "The installer will automatically detect if you have root privileges:"
    echo "  • With root: System-wide installation in /opt"
    echo "  • Without root: User installation in ~/.local"
}

# Parse command line arguments
case "${1:-}" in
    --uninstall)
        check_root
        uninstall
        ;;
    --help)
        show_help
        ;;
    --install|"")
        install
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac

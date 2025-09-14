# Auto Typer - Modern Text Automation Tool

A cross-platform desktop application for automated text typing with a sleek, modern interface built using CustomTkinter.

## 🚀 Quick Start

### Option 1: Download Pre-built Installer (Recommended)

#### Windows
1. Download `AutoTyper-Setup.exe` from the releases
2. Run the installer and follow the setup wizard
3. Launch from Start Menu or Desktop shortcut

#### Linux
1. Download the appropriate package:
   - **Ubuntu/Debian**: `auto-typer_1.0.0_amd64.deb`
   - **Universal Linux**: `AutoTyper-x86_64.AppImage`
   - **Portable**: `AutoTyper-Portable-Linux.tar.gz`

2. Install:
   ```bash
   # For .deb package
   sudo dpkg -i auto-typer_1.0.0_amd64.deb
   
   # For AppImage
   chmod +x AutoTyper-x86_64.AppImage
   ./AutoTyper-x86_64.AppImage
   
   # For portable version
   tar -xzf AutoTyper-Portable-Linux.tar.gz
   cd AutoTyper-Portable
   ./AutoTyper
   ```

### Option 2: Build from Source

#### Prerequisites
- Python 3.8 or higher
- Git (optional)

#### Quick Setup
```bash
# Clone or download the repository
git clone https://github.com/dovndev/Putoper.git
cd Putoper

# Run the setup script
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Run the application
python auto_typing.py
```

#### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python auto_typing.py
```

## 🔨 Building Distributables

### All Platforms
```bash
# Activate virtual environment
source .venv/bin/activate

# Install build dependencies
pip install pyinstaller

# Build all packages
python build.py

# Or build specific packages
python build.py exe      # Executable only
python build.py windows  # Windows installer (Windows only)
python build.py linux    # Linux packages (Linux only)
python build.py portable # Portable archive
```

### Linux Installation from Source
```bash
# Build the executable first
python build.py exe

# Install system-wide
sudo ./install.sh
```

## 📋 Features

### Core Features
- **Modern GUI**: Clean, responsive interface with system theme support
- **Smart Typing**: Character-by-character typing with configurable speed
- **Loop Mode**: Repeat text continuously for testing or demonstrations
- **Delay Control**: Customizable delay before typing starts
- **Speed Settings**: Four speed presets from slow to instant
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Interface Features
- **Dark/Light Mode**: Automatic system theme detection
- **Responsive Design**: Resizable window with proper scaling
- **Status Indicators**: Real-time feedback on typing status
- **Background Operation**: Minimizes during typing
- **Error Handling**: Graceful error recovery

## 🎯 Usage Guide

### Basic Usage
1. **Enter Text**: Type or paste your text in the main text area
2. **Set Delay**: Configure the delay before typing starts (default: 3 seconds)
3. **Choose Speed**: Select typing speed from the dropdown menu
4. **Optional Settings**:
   - Enable **Loop Mode** for continuous repetition
   - Adjust speed for different typing patterns
5. **Start Typing**: Click "Start Typing" button
6. **Quick Focus**: Click on your target application within the delay period
7. **Emergency Stop**: Press the "Stop" button if needed

### Speed Settings
- **Slow**: 0.1s between characters (for demonstrations)
- **Normal**: 0.02s between characters (human-like typing)
- **Fast**: 0.005s between characters (quick input)
- **Instant**: No delay (immediate output)

### Tips & Best Practices
- **Target Application**: Ensure your target application window is ready to receive text
- **Text Formatting**: The app preserves your original text formatting
- **Special Characters**: All Unicode characters are supported
- **Long Text**: No limit on text length - memory permitting

## 🛠️ Development

### Project Structure
```
Putoper/
├── auto_typing.py      # Main application file
├── requirements.txt    # Python dependencies
├── build.py           # Build script for distributables
├── setup.sh           # Quick setup script (Linux/macOS)
├── install.sh         # System installation script (Linux)
├── README.md          # This file
├── .venv/             # Virtual environment (created by setup)
├── dist/              # Built executables
├── build/             # Build artifacts
└── installers/        # Final installer packages
```

### Dependencies
- **customtkinter**: Modern GUI framework
- **pyautogui**: Cross-platform automation library
- **darkdetect**: System theme detection
- **packaging**: Version management

## 🐛 Troubleshooting

### Common Issues

#### "Module not found" Error
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### PyAutoGUI Not Working
```bash
# Linux: Install required system packages
sudo apt install python3-tk python3-dev

# macOS: Install Xcode Command Line Tools
xcode-select --install
```

### System Requirements

#### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux with X11
- **RAM**: 100 MB
- **Storage**: 50 MB free space
- **Python**: 3.8+ (for source builds)

## 📄 License

This project is licensed under the MIT License.

## 🤝 Support

Created by dovndev

---

**Made with ❤️ for the automation community**

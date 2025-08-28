# Auto Typer - Modern Text Automation Tool

A modern, cross-platform application for automated text typing with a sleek CustomTkinter interface.

## 🐍 Running with Python (Recommended)

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start
```bash
# Clone or download the repository
git clone https://github.com/dovndev/Putoper.git
cd Putoper

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python auto_typing.py
```

### Alternative: Direct Python Run
If you already have the dependencies installed globally:
```bash
# Install dependencies
pip install customtkinter pyautogui

# Run the application
python auto_typing.py
```

## ✨ Features

- **Modern GUI** - Clean, contemporary interface with dark/light theme support
- **Customizable Delay** - Set typing delay before execution
- **Loop Mode** - Enable continuous text typing
- **Threading Support** - Non-blocking GUI during typing operations
- **Character-by-Character Typing** - Preserves exact text formatting and indentation
- **Cross-Platform** - Works on Windows, Linux, and macOS
- **No Auto-Formatting** - Types text exactly as entered without modifications

## 📦 Alternative Installation Methods

### Linux (.tar.gz)
1. Extract the package: `tar -xzf auto-typer-linux-v1.0.tar.gz`
2. Navigate to the directory: `cd auto-typer-linux-v1.0/`
3. Run the installer: `sudo ./install.sh`

### Windows (.exe)
1. Download `auto_typer_windows.exe`
2. Double-click to run (no installation required)

## 🚀 Usage

1. **Launch the application**
   - Python method: `python auto_typing.py` (recommended)
   - Linux: Run `auto-typer` from terminal or find "Auto Typer" in applications menu
   - Windows: Double-click the .exe file

2. **Enter your text** in the text area
3. **Set delay** (seconds before typing starts)
4. **Enable loop mode** if you want continuous typing
5. **Click "Start Typing"**
6. **Quickly switch** to your target window
7. **Text will be typed automatically** after the delay

## 💡 Tips for Best Results

- **Use adequate delay** (3-5 seconds) to switch to target window
- **Disable auto-formatting** in target applications (like VS Code) for exact reproduction
- **Test with simple text** first before using with complex code
- **Loop mode** is useful for repetitive typing tasks

## 📋 System Requirements

### For Python Installation
- **Python**: 3.8 or higher
- **Operating System**: Windows 7+, Linux (any modern distro), macOS 10.12+
- **Dependencies**: customtkinter, pyautogui (auto-installed with pip)

### For Standalone Executables

### For Standalone Executables

#### Linux
- glibc 2.17 or later
- X11 display server
- libx11-6

#### Windows
- Windows 7 or later
- No additional dependencies required

## 🛠️ Development

### Project Structure
```
Putoper/
├── auto_typing.py          # Main application file
├── dist/                   # Built executables
├── .venv/                  # Virtual environment
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

### Building Executables
```bash
# Install PyInstaller
pip install pyinstaller

# Build Linux executable
pyinstaller --onefile --noconsole auto_typing.py

# Build Windows executable (cross-platform)
pyinstaller --onefile --noconsole auto_typing.py --name auto_typer_windows
```

## Author

Created by dovndev

## License

This project is distributed as-is for personal and educational use.

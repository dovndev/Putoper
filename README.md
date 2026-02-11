# Auto Typer - Native Text Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-blue.svg)](https://www.linux.org/)
[![Python: 3.x](https://img.shields.io/badge/Python-3.x-green.svg)](https://www.python.org/)

A lightweight, system-native application for automated typing on Linux. It simulates keyboard input to "type" text into other applications, useful for demos, presentations, or pasting into restricted fields.

## ✨ Features

- **Zero External Dependencies**: Uses your system's built-in Python 3, GTK 3, and X11 libraries
- **Single File App**: Compiles into a single `AutoTyper` executable
- **Native Performance**: Light on resources, integrates seamlessly with your system theme
- **Simple & Intuitive**: Clean GTK3 interface with configurable typing delay
- **X11 Compatible**: Works on X11 and Wayland (via XWayland)

## 📸 Demo

> *Coming soon: Screenshot and demo GIF*

## 🛠️ Requirements

**Operating System:**
- Linux with X11 (Wayland support via XWayland)

**System Dependencies** (pre-installed on most distros):
- **Python 3** - Default on most distributions
- **GTK 3** - Default on GNOME/XFCE/MATE/Cinnamon desktops
  - Package: `python3-gi` or `python-gobject`
- **X11 Libraries**:
  - `libx11-6`
  - `libxtst6`

## 📥 Installation

### Option 1: Portable App (Recommended)

1. Download the **AutoTyper** executable from [Releases](https://github.com/dovndev/Putoper/releases)
2. Make it executable:
   ```bash
   chmod +x AutoTyper
   ```
3. Run it:
   ```bash
   ./AutoTyper
   ```

### Option 2: Build from Source

```bash
# 1. Clone the repository
git clone https://github.com/dovndev/Putoper.git
cd Putoper

# 2. Build the application
./create-packages.sh

# 3. Run from packages directory
./packages/AutoTyper
```

## 🎯 Usage

1. Launch the application
2. Enter the text you want to auto-type
3. Set the delay (in seconds) before typing starts
4. Click "Start Auto Typing"
5. Switch to your target application
6. The text will be automatically typed after the delay

## 🏗️ Development

### Project Structure

- **`auto_typing_gtk.py`** - Main GUI logic (GTK3)
- **`x11_input.py`** - Keyboard simulation logic (ctypes/X11)
- **`build.py`** - Script to bundle the app using `zipapp`
- **`create-packages.sh`** - Build script for creating distributable packages

### Building

The application uses Python's `zipapp` module to create a self-contained executable:

```bash
./create-packages.sh
```

This creates a portable `AutoTyper` executable in the `packages/` directory.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with native Linux technologies:
- GTK 3 for the user interface
- X11/XTest for keyboard simulation
- Python 3 for application logic

---

**Made with ❤️ for the Linux community**

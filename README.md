# Auto Typer - Native Text Automation

A lightweight, system-native application for automated typing on Linux.
It simulates keyboard input to "type" text into other applications, useful for demos or pasting into restricted fields.

## 🚀 Features
*   **Zero External Dependencies**: Uses your system's built-in Python 3, GTK 3, and X11 libraries.
*   **Single File App**: Compiles into a single `AutoTyper` executable.
*   **Native Performance**: Light on resources, integrates with system theme.

## 🛠️ Requirements
*   **Linux** with X11 (Wayland support via XWayland).
*   **Python 3** (Default on most distros).
*   **GTK 3** (Default on GNOME/XFCE/MATE/Cinnamon desktops).
    *   Package: `python3-gi` or `python-gobject`.
*   **X11 Libraries**:
    *   `libx11-6`
    *   `libxtst6`

## 📥 Installation

### Option 1: Portable App (Recommended)
1.  Download the **AutoTyper** file (or `AutoTyper-Linux-Portable.zip`).
2.  Make it executable: `chmod +x AutoTyper`
3.  Run it: `./AutoTyper`

### Option 2: Build from Source
```bash
# 1. Clone
git clone https://github.com/dovndev/Putoper.git
cd Putoper

# 2. Build
./create-packages.sh

# 3. Runs from packages/AutoTyper
./packages/AutoTyper
```

## 🏗️ Development
*   **`auto_typing_gtk.py`**: Main GUI logic (GTK3).
*   **`x11_input.py`**: Keyboard simulation logic (ctypes/X11).
*   **`build.py`**: Script to bundle the app using `zipapp`.

**License**: MIT

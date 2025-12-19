# Installation Guide

## System Dependencies (Linux)

PyQt5 requires certain system libraries to work properly. If you encounter the "Could not load the Qt platform plugin 'xcb'" error, install the following packages:

### Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxrender1 \
    libfontconfig1 \
    libx11-xcb1
```

### Fedora/RHEL/CentOS:

```bash
sudo dnf install -y \
    libxcb \
    libxcb-xinerama \
    libxcb-cursor \
    libxcb-render-util \
    libxcb-xfixes \
    libxkbcommon \
    libxkbcommon-x11 \
    libXrender \
    fontconfig \
    libX11-xcb
```

### Arch Linux:

```bash
sudo pacman -S \
    libxcb \
    libxcb-xinerama \
    libxcb-cursor \
    libxkbcommon \
    libxkbcommon-x11 \
    libxrender \
    fontconfig
```

## Python Dependencies

After installing system dependencies, install Python packages:

```bash
pip install -r requirements.txt
```

## Verification

Test if PyQt5 works:

```bash
python3 -c "from PyQt5.QtWidgets import QApplication; import sys; app = QApplication(sys.argv); print('PyQt5 is working!')"
```

If this command runs without errors, you're ready to use Screen Keeper!


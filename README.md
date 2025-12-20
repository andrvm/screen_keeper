# Screen Keeper

A cross-platform desktop application built with Python and PyQt5 that prevents your computer from sleeping and keeps the screen alive.

## Features

- **Prevent System Sleep**: Uses system APIs to prevent sleep on Windows and Linux
- **Activity Detection**: Monitors mouse and keyboard activity to detect user inactivity
- **Smart Mouse Movement**: Automatically moves the mouse cursor when user is inactive to keep screen on
- **System Tray Support**: Minimize to system tray and control from there
- **Cross-Platform**: Works on both Windows and Linux

## Installation

### Requirements

- Python 3.7 or higher
- PyQt5
- pynput

### Setup

1. Clone or download this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python -m screen_keeper.main
```

Or if you prefer:

```bash
python screen_keeper/main.py
```

### How It Works

1. **Start the application** and configure your settings:
   - **Inactivity Timeout**: Time in seconds before considering user inactive (default: 60s)
   - **Mouse Movement Interval**: How often to move the mouse when inactive (default: 30s)
   - **Prevent System Sleep**: Enable system-level sleep prevention
   - **Use Activity Detection**: Enable smart detection - only move mouse when inactive

2. **Click "Start"** to begin keeping your screen alive

3. The application will:
   - Monitor your mouse and keyboard activity
   - When inactive, start moving the mouse cursor by 1 pixel to prevent screen timeout
   - When you become active again, stop moving the mouse
   - Optionally prevent system sleep using OS APIs

4. **Minimize to Tray**: Close the window to minimize to system tray (if available)

## Configuration

Settings are automatically saved to `~/.screen-keeper/config.json` (Linux) or `%USERPROFILE%\.screen-keeper\config.json` (Windows).

## Technical Details

### Sleep Prevention

- **Windows**: Uses `SetThreadExecutionState` API to prevent sleep
- **Linux**: Relies primarily on mouse movement (systemd-inhibit could be added for full support)

### Activity Monitoring

- Uses `pynput` library to monitor mouse and keyboard events
- Detects inactivity based on configurable timeout
- Automatically starts/stops mouse movement based on activity

### Mouse Movement

- Moves cursor by 1 pixel (configurable) in random direction
- Immediately returns to original position
- Barely noticeable but effective at preventing screen timeout

## Troubleshooting

### Qt Platform Plugin Error (Linux)

If you encounter the error:
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
```

This means PyQt5 is missing required system libraries. Install them:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libx11-xcb1
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install -y \
    libxcb-xinerama \
    libxcb-cursor \
    libxkbcommon \
    libxkbcommon-x11 \
    libX11-xcb
```

**Arch Linux:**
```bash
sudo pacman -S \
    libxcb-xinerama \
    libxcb-cursor \
    libxkbcommon \
    libxkbcommon-x11
```

### Windows Installation

On Windows, the application should work out of the box after installing Python dependencies:

```bash
pip install -r requirements.txt
```

**Note**: On Windows 10/11, you may see a Windows Defender SmartScreen warning when running Python scripts. This is normal for unsigned executables. You can safely allow it to run.

**System Requirements**:
- Windows 7 or later
- Python 3.7 or higher
- No additional system libraries needed (unlike Linux)

### Permission Issues (Linux)

On some Linux systems, you may need to grant permissions for:
- Mouse/keyboard monitoring (usually automatic)
- System sleep prevention (may require additional setup)

### Mouse Movement Not Working

- Ensure the application window is not minimized or hidden
- Check that no other application is blocking mouse control
- Try running with administrator/sudo privileges if needed
- On Windows, ensure no antivirus is blocking mouse control

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues and enhancement requests!


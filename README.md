# Screen Keeper

A cross-platform desktop application built with Python and PyQt5 that prevents your computer from sleeping and keeps the screen alive.

## Features

- **Prevent System Sleep**: Uses system APIs to prevent sleep on Windows and Linux with periodic reassertion for Windows 10/11
- **Activity Detection**: Monitors mouse and keyboard activity to detect user inactivity
- **Multiple Activity Simulation Modes**: Choose between mouse movement, keyboard input, or both
- **SecretNet Compatible**: Keyboard simulation mode works with SecretNet and other security software
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
   - **Mouse Movement Interval**: How often to simulate activity when inactive (default: 30s)
   - **Activity Simulation**: Choose simulation mode (default: Both)
     - **Mouse Movement**: Move cursor slightly
     - **Keyboard Input**: Toggle Scroll Lock (for SecretNet like software)
     - **Both (Recommended)**: Use both methods for maximum compatibility
   - **Prevent System Sleep**: Enable system-level sleep prevention
   - **Use Activity Detection**: Enable smart detection - only simulate activity when inactive

2. **Click "Start"** to begin keeping your screen alive

3. The application will:
   - Monitor your mouse and keyboard activity
   - When inactive, simulate activity based on selected mode:
     - Move mouse cursor by 1 pixel (barely noticeable)
     - Toggle Scroll Lock key (no visible effect)
   - When you become active again, stop simulating activity
   - Prevent system sleep using OS APIs (with periodic reassertion on Windows)

4. **Minimize to Tray**: Close the window to minimize to system tray (if available)

## Configuration

Settings are automatically saved to `~/.screen-keeper/config.json` (Linux) or `%USERPROFILE%\.screen-keeper\config.json` (Windows).

## Technical Details

### Sleep Prevention

- **Windows**: Uses `SetThreadExecutionState` API with periodic reassertion every 30 seconds for Windows 10/11 compatibility
- **Linux**: Relies primarily on activity simulation (systemd-inhibit could be added for full support)

### Activity Monitoring

- Uses `pynput` library to monitor mouse and keyboard events
- Detects inactivity based on configurable timeout
- Automatically starts/stops activity simulation based on user activity

### Activity Simulation

**Mouse Movement Mode:**
- Moves cursor by 1 pixel in random direction
- Immediately returns to original position
- Barely noticeable but effective at preventing screen timeout

**Keyboard Input Mode:**
- Toggles Scroll Lock key twice (on then off)
- No visible effect or text input
- Detected as real activity by security software like SecretNet

**Both Mode (Recommended):**
- Combines both methods for maximum compatibility
- Works with standard Windows/Linux power management and security software

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

### Activity Simulation Not Working

- Ensure the application window is not minimized or hidden
- Check that no other application is blocking input control
- Try running with administrator/sudo privileges if needed
- On Windows, ensure no antivirus is blocking input simulation

### Working with Security Software (SecretNet, etc.)

If you're using security software that monitors user activity:

1. **Select "Keyboard Input" or "Both" mode** in Activity Simulation settings
2. **Start the application** and wait for the security software's inactivity timeout
3. **Verify** that the screen doesn't lock
4. If Scroll Lock LED on your keyboard blinks briefly, that's normal (it toggles on/off)
5. If keyboard mode doesn't work, try "Both" mode for redundancy

**Note**: The application simulates real keyboard input that security software will detect as user activity.

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues and enhancement requests!


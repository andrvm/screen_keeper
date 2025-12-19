# Build Instructions

## Environment Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```

2.  Activate the virtual environment:
    *   **Linux**: `source venv/bin/activate`
    *   **Windows**: `venv\Scripts\activate`

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Building Executable

### Linux

To build a standalone executable on Linux:

```bash
pyinstaller --name "screen-keeper" \
            --onefile \
            --windowed \
            --add-data "resources:resources" \
            --hidden-import "pynput.keyboard._xorg" \
            --hidden-import "pynput.mouse._xorg" \
            run.py
```

After building, the executable will be located in the `dist` directory.

### Windows

To build a standalone executable on Windows:

```powershell
pyinstaller --name "screen-keeper" `
            --onefile `
            --windowed `
            --add-data "resources;resources" `
            --hidden-import "pynput.keyboard._win32" `
            --hidden-import "pynput.mouse._win32" `
            run.py
```

Note the difference in `--add-data` separator (`;` instead of `:`) and line continuation character (`` ` `` instead of `\`).

After building, the executable will be located in the `dist` directory.

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

Or use the script `linux_build.sh`.

```bash
./linux_build.sh
```

After building, the executable will be located in the `dist` directory.

### Windows

To build a standalone executable on Windows (not tested yet):

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

Or build the .exe file in Linux using Docker (remove "optimize=0" from the spec file):

```bash
docker run --rm -v "$(pwd):/src/" -v wine_home:/root/.wine cdrx/pyinstaller-windows
```

Add this param to the spec file to build the app with icon:
* icon=['resources/icons/app.ico']

After building, the executable will be located in the `dist` directory.

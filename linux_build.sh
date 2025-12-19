pyinstaller --name "screen-keeper" \
            --onefile \
            --windowed \
            --add-data "resources:resources" \
            --hidden-import "pynput.keyboard._xorg" \
            --hidden-import "pynput.mouse._xorg" \
            run.py
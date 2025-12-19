"""
Main entry point for Screen Keeper application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from screen_keeper.gui.main_window import MainWindow


def main():
    """Main function to start the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Screen Keeper")
    app.setOrganizationName("Screen Keeper")
    
    # Check if system tray is available
    if not QApplication.instance().isSessionRestored():
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()


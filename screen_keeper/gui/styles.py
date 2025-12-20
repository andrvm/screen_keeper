"""
Modern Dark Theme QSS Styles for Screen Keeper.
"""

DARK_THEME = """
/* Main Window */
QMainWindow {
    background-color: #2b2b2b;
    color: #e0e0e0;
}

QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Group Box */
QGroupBox {
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    margin-top: 24px;
    background-color: #333333;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: #4CAF50;
}

/* Labels */
QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

/* Buttons */
QPushButton {
    background-color: #404040;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #505050;
}

QPushButton:pressed {
    background-color: #2d2d2d;
}

QPushButton:disabled {
    background-color: #2d2d2d;
    color: #666666;
}

/* Specific Buttons */
QPushButton#start_btn {
    background-color: #4CAF50;
    color: #ffffff;
}

QPushButton#start_btn:hover {
    background-color: #45a049;
}

QPushButton#start_btn:pressed {
    background-color: #388E3C;
}

QPushButton#start_btn:disabled {
    background-color: #2d2d2d;
    color: #666666;
    border: 1px solid #3d3d3d;
}

QPushButton#stop_btn {
    background-color: #f44336;
    color: #ffffff;
}

QPushButton#stop_btn:hover {
    background-color: #e53935;
}

QPushButton#stop_btn:pressed {
    background-color: #d32f2f;
}

QPushButton#stop_btn:disabled {
    background-color: #2d2d2d;
    color: #666666;
    border: 1px solid #3d3d3d;
}
   
/* Inputs */
QSpinBox, QDoubleSpinBox {
    background-color: #404040;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 4px;
    color: #ffffff;
    selection-background-color: #4CAF50;
}

QSpinBox::up-button, QDoubleSpinBox::up-button, 
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #505050;
    border: none;
    border-radius: 2px;
    width: 16px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, 
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #606060;
}

/* Checkbox */
QCheckBox {
    spacing: 8px;
    background-color: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 1px solid #505050;
    background-color: #404040;
}

QCheckBox::indicator:checked {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

QCheckBox::indicator:hover {
    border-color: #4CAF50;
}

/* Menu Bar */
QMenuBar {
    background-color: #333333;
    color: #e0e0e0;
    border-bottom: 1px solid #3d3d3d;
}

QMenuBar::item {
    padding: 8px 12px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #404040;
}

QMenu {
    background-color: #333333;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
}

QMenu::item {
    padding: 8px 24px 8px 12px;
}

QMenu::item:selected {
    background-color: #404040;
}

/* Status Bar */
QStatusBar {
    background-color: #333333;
    color: #999999;
}
"""

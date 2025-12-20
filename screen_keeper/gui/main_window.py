"""
Main GUI window for Screen Keeper application.
"""

import sys
import os
from pathlib import Path
from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSpinBox, QDoubleSpinBox, QCheckBox,
    QMessageBox, QGroupBox, QStatusBar, QSystemTrayIcon, QMenu, QAction,
    QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon

from screen_keeper.core.sleep_preventer import SleepPreventer
from screen_keeper.core.activity_monitor import ActivityMonitor
from screen_keeper.core.mouse_mover import MouseMover
from screen_keeper.config.settings import Settings
from screen_keeper.gui.styles import DARK_THEME



class MainWindow(QMainWindow):
    """Main application window."""
    
    def get_resource_path(self, relative_path: str) -> str:
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
            
        return os.path.join(base_path, relative_path)
    
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.sleep_preventer = SleepPreventer()
        self.activity_monitor: Optional[ActivityMonitor] = None
        self.mouse_mover: Optional[MouseMover] = None
        self.is_running = False

        
        self.init_ui()
        self.load_settings()
        
        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Update every second
        
        # System tray
        self.setup_system_tray()
        
        # Menu Bar
        self.setup_menu_bar()
        
        # Apply Styles
        self.apply_styles()
        
        # Auto Start Logic
        if self.settings.get("auto_start_keeping", True):
            self.start_keeping()
            # Minimize to tray if auto-started
            QTimer.singleShot(0, self.hide)
            if hasattr(self, "tray_icon"):
                self.tray_icon.showMessage(
                    "Screen Keeper",
                    "Application started active and minimized to tray",
                    QSystemTrayIcon.Information,
                    2000
                )
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Screen Keeper")
        
        # Set window icon
        icon_path = self.get_resource_path(os.path.join("resources", "icons", "app.png"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        # self.setGeometry(100, 100, 500, 600) # Removed fixed size
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Screen Keeper")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Status group
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px; padding: 5px;")
        status_layout.addWidget(self.status_label)
        
        self.activity_label = QLabel("Activity: Monitoring...")
        self.activity_label.setStyleSheet("font-size: 12px; color: #666;")
        status_layout.addWidget(self.activity_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Settings group
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        
        # Inactivity timeout
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Inactivity Timeout (seconds):"))
        self.inactivity_timeout_spin = QDoubleSpinBox()
        self.inactivity_timeout_spin.setRange(10.0, 600.0)
        self.inactivity_timeout_spin.setSuffix(" sec")
        self.inactivity_timeout_spin.setDecimals(0)
        timeout_layout.addWidget(self.inactivity_timeout_spin)
        settings_layout.addLayout(timeout_layout)
        
        # Mouse movement interval
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Mouse Movement Interval (seconds):"))
        self.movement_interval_spin = QDoubleSpinBox()
        self.movement_interval_spin.setRange(5.0, 300.0)
        self.movement_interval_spin.setSuffix(" sec")
        self.movement_interval_spin.setDecimals(0)
        interval_layout.addWidget(self.movement_interval_spin)
        settings_layout.addLayout(interval_layout)
        
        # Checkboxes
        self.prevent_sleep_check = QCheckBox("Prevent System Sleep")
        self.prevent_sleep_check.setChecked(True)
        settings_layout.addWidget(self.prevent_sleep_check)
        
        self.activity_detection_check = QCheckBox("Use Activity Detection")
        self.activity_detection_check.setChecked(True)
        settings_layout.addWidget(self.activity_detection_check)
        
        self.auto_start_check = QCheckBox("Auto-start Active & Minimized")
        self.auto_start_check.setToolTip("Automatically start keeping screen alive and minimize to tray on launch")
        settings_layout.addWidget(self.auto_start_check)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.start_keeping)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop_keeping)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Adjust size to fit content
        self.adjustSize()
    
    def setup_system_tray(self):
        """Setup system tray icon."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set tray icon
        icon_path = self.get_resource_path(os.path.join("resources", "icons", "app.png"))
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
        
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Handle system tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()
    
    def load_settings(self):
        """Load settings into UI."""
        self.inactivity_timeout_spin.setValue(self.settings.get("inactivity_timeout", 60.0))
        self.movement_interval_spin.setValue(self.settings.get("mouse_movement_interval", 30.0))
        self.prevent_sleep_check.setChecked(self.settings.get("prevent_sleep", True))
        self.activity_detection_check.setChecked(self.settings.get("use_activity_detection", True))
        self.auto_start_check.setChecked(self.settings.get("auto_start_keeping", True))
    
    def save_settings(self):
        """Save current UI settings."""
        self.settings.set("inactivity_timeout", self.inactivity_timeout_spin.value())
        self.settings.set("mouse_movement_interval", self.movement_interval_spin.value())
        self.settings.set("prevent_sleep", self.prevent_sleep_check.isChecked())
        self.settings.set("use_activity_detection", self.activity_detection_check.isChecked())
        self.settings.set("auto_start_keeping", self.auto_start_check.isChecked())
        self.settings.save()
    
    def start_keeping(self):
        """Start keeping screen alive."""
        if self.is_running:
            return
        
        self.save_settings()
        
        # Prevent sleep if enabled
        if self.prevent_sleep_check.isChecked():
            if not self.sleep_preventer.prevent_sleep():
                QMessageBox.warning(self, "Warning", "Failed to prevent system sleep. Mouse movement will still work.")
        
        # Setup activity monitoring if enabled
        if self.activity_detection_check.isChecked():
            self.activity_monitor = ActivityMonitor(
                inactivity_timeout=self.inactivity_timeout_spin.value()
            )
            self.activity_monitor.set_inactivity_callback(self.on_user_inactive)
            self.activity_monitor.set_activity_callback(self.on_user_active)
            
            if not self.activity_monitor.start():
                QMessageBox.warning(self, "Warning", "Failed to start activity monitoring. Mouse will move continuously.")
                self.activity_monitor = None
        
        # Setup mouse mover
        self.mouse_mover = MouseMover(
            interval=self.movement_interval_spin.value()
        )
        
        # Start mouse mover based on activity detection
        if self.activity_detection_check.isChecked() and self.activity_monitor:
            # Only move when inactive
            pass  # Will be started in on_user_inactive callback
        else:
            # Move continuously
            if not self.mouse_mover.start():
                QMessageBox.critical(self, "Error", "Failed to start mouse movement.")
                self.stop_keeping()
                return
        
        self.is_running = True
        self.update_ui_state()
        self.statusBar().showMessage("Screen Keeper is active")
    
    def update_ui_state(self):
        """Update UI elements based on running state."""
        self.start_btn.setEnabled(not self.is_running)
        self.stop_btn.setEnabled(self.is_running)
        
        # Disable settings when running
        self.inactivity_timeout_spin.setEnabled(not self.is_running)
        self.movement_interval_spin.setEnabled(not self.is_running)
        self.prevent_sleep_check.setEnabled(not self.is_running)
        self.activity_detection_check.setEnabled(not self.is_running)
        self.auto_start_check.setEnabled(not self.is_running)
    
    def stop_keeping(self):
        """Stop keeping screen alive."""
        if not self.is_running:
            return
        
        # Stop mouse mover
        if self.mouse_mover:
            self.mouse_mover.stop()
            self.mouse_mover = None
        
        # Stop activity monitor
        if self.activity_monitor:
            self.activity_monitor.stop()
            self.activity_monitor = None
        
        # Allow sleep
        self.sleep_preventer.allow_sleep()
        
        self.is_running = False
        self.update_ui_state()
        self.statusBar().showMessage("Screen Keeper stopped")
    
    def on_user_inactive(self):
        """Called when user becomes inactive."""
        if self.mouse_mover and not self.mouse_mover.is_running:
            self.mouse_mover.start()
    
    def on_user_active(self):
        """Called when user becomes active."""
        if self.mouse_mover and self.mouse_mover.is_running:
            self.mouse_mover.stop()
    
    def update_status(self):
        """Update status display."""
        if self.is_running:
            self.status_label.setText("Status: Running")
            
            if self.activity_monitor:
                if self.activity_monitor.is_inactive:
                    self.activity_label.setText(
                        f"Activity: Inactive ({int(self.activity_monitor.time_since_activity)}s)"
                    )
                    self.activity_label.setStyleSheet("font-size: 12px; color: #f44336;")
                else:
                    self.activity_label.setText("Activity: Active")
                    self.activity_label.setStyleSheet("font-size: 12px; color: #4CAF50;")
            else:
                self.activity_label.setText("Activity: Continuous mode")
                self.activity_label.setStyleSheet("font-size: 12px; color: #2196F3;")
        else:
            self.status_label.setText("Status: Stopped")
            self.activity_label.setText("Activity: Not monitoring")
            self.activity_label.setStyleSheet("font-size: 12px; color: #666;")
    
    
    def setup_menu_bar(self):
        """Setup application menu bar."""
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)
        
        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.setStatusTip("About Screen Keeper")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def apply_styles(self):
        """Apply modern dark theme."""
        self.setStyleSheet(DARK_THEME)
        
        # Specific button styling if needed, but QSS handles most classes
        pass

    def closeEvent(self, event):
        """Handle window close event."""
        # Clean up existing close logic to simpler "Minimize to Tray"
        # The user requested: "The close icon must put the app in the tray."
        
        if self.tray_icon.isVisible():
            QMessageBox.information(
                self,
                "Screen Keeper",
                "The application will keep running in the system tray. To exit completely, use File -> Exit.",
                QMessageBox.Ok
            )
            self.hide()
            event.ignore()
        else:
            # If no tray, we must verify exit or just close
             reply = QMessageBox.question(
                self,
                "Screen Keeper",
                "Exit Screen Keeper?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
             if reply == QMessageBox.Yes:
                 self.close_application()
                 event.accept()
             else:
                 event.ignore()

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Screen Keeper",
            "Screen Keeper v1.1\n\n"
            "A tool to prevent your computer from going to sleep.\n\n"
            "Features:\n"
            "- Prevent System Sleep\n"
            "- Activity Detection\n"
            "- Smart Mouse Movement\n"
            "- System Tray Support"
        )

    def close_application(self):
        """Close application completely."""
        self.stop_keeping()
        QApplication.quit()


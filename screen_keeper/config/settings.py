"""
Configuration management module.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Settings:
    """Manages application settings."""
    
    DEFAULT_SETTINGS = {
        "inactivity_timeout": 60.0,  # seconds
        "mouse_movement_interval": 30.0,  # seconds
        "movement_distance": 1,  # pixels
        "prevent_sleep": True,
        "use_activity_detection": True,
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings.
        
        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            # Use user's home directory for config
            config_dir = Path.home() / ".screen-keeper"
            config_dir.mkdir(exist_ok=True)
            config_file = str(config_dir / "config.json")
        
        self.config_file = config_file
        self._settings = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self) -> None:
        """Load settings from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._settings.update(loaded_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")
                # Keep defaults
    
    def save(self) -> bool:
        """Save settings to file."""
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, "w") as f:
                json.dump(self._settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self._settings[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings as a dictionary."""
        return self._settings.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._settings = self.DEFAULT_SETTINGS.copy()


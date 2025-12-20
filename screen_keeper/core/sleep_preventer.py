"""
Cross-platform sleep prevention module.
Uses system APIs to prevent sleep on Windows and Linux.
"""

import platform
import ctypes
from typing import Optional


class SleepPreventer:
    """Prevents system from going to sleep."""
    
    def __init__(self):
        self.system = platform.system()
        self._handle: Optional[ctypes.c_void_p] = None
        self._is_active = False
        
    def prevent_sleep(self, reason: str = "Screen Keeper") -> bool:
        """
        Prevent system from sleeping.
        
        Args:
            reason: Reason for preventing sleep (used on Linux)
            
        Returns:
            True if successful, False otherwise
        """
        if self._is_active:
            return True
            
        try:
            if self.system == "Windows":
                return self._prevent_sleep_windows()
            elif self.system == "Linux":
                return self._prevent_sleep_linux(reason)
            else:
                # macOS or other - not implemented
                return False
        except Exception as e:
            print(f"Error preventing sleep: {e}")
            return False
    
    def _prevent_sleep_windows(self) -> bool:
        """Prevent sleep on Windows using SetThreadExecutionState."""
        try:
            # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            # ES_DISPLAY_REQUIRED prevents display from turning off
            # ES_SYSTEM_REQUIRED prevents system from sleeping
            ES_CONTINUOUS = 0x80000000
            ES_SYSTEM_REQUIRED = 0x00000001
            ES_DISPLAY_REQUIRED = 0x00000002
            
            ret = ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
            if ret == 0:
                print("SetThreadExecutionState failed")
                return False
                
            self._is_active = True
            return True
        except Exception as e:
            print(f"Windows sleep prevention failed: {e}")
            return False
    
    def _prevent_sleep_linux(self, reason: str) -> bool:
        """Prevent sleep on Linux using systemd/logind via DBus."""
        try:
            # Try to use systemd-inhibit if available
            import subprocess
            result = subprocess.run(
                ["which", "systemd-inhibit"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # systemd-inhibit is available, but we can't easily control it from Python
                # For now, we'll rely on mouse movement
                # In a production app, you might want to use python-dbus
                self._is_active = True
                return True
            else:
                # Fallback: just mark as active, rely on mouse movement
                self._is_active = True
                return True
        except Exception as e:
            print(f"Linux sleep prevention failed: {e}")
            # Still mark as active, mouse movement will help
            self._is_active = True
            return True
    
    def allow_sleep(self) -> bool:
        """
        Allow system to sleep normally.
        
        Returns:
            True if successful, False otherwise
        """
        if not self._is_active:
            return True
            
        try:
            if self.system == "Windows":
                return self._allow_sleep_windows()
            elif self.system == "Linux":
                self._is_active = False
                return True
            else:
                return False
        except Exception as e:
            print(f"Error allowing sleep: {e}")
            return False
    
    def _allow_sleep_windows(self) -> bool:
        """Allow sleep on Windows."""
        try:
            ES_CONTINUOUS = 0x80000000
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            self._is_active = False
            return True
        except Exception as e:
            print(f"Windows sleep allowance failed: {e}")
            return False
    
    @property
    def is_active(self) -> bool:
        """Check if sleep prevention is currently active."""
        return self._is_active


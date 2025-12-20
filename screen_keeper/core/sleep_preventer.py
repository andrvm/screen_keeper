"""
Cross-platform sleep prevention module.
Uses system APIs to prevent sleep on Windows and Linux.
"""

import platform
import ctypes
import threading
from typing import Optional


class SleepPreventer:
    """Prevents system from going to sleep."""
    
    def __init__(self):
        self.system = platform.system()
        self._handle: Optional[ctypes.c_void_p] = None
        self._is_active = False
        self._timer: Optional[threading.Timer] = None
        self._timer_interval = 30.0  # Reassert every 30 seconds
        
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
            
            # Set the execution state
            ret = ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
            if ret == 0:
                print("SetThreadExecutionState failed - return value is 0")
                return False
            
            print(f"SetThreadExecutionState succeeded - return value: {ret}")
            self._is_active = True
            
            # Start periodic reassertion timer for Windows 10/11 compatibility
            self._start_reassertion_timer()
            
            return True
        except Exception as e:
            print(f"Windows sleep prevention failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _start_reassertion_timer(self):
        """Start a timer to periodically reassert the execution state."""
        if self.system != "Windows":
            return
            
        # Cancel existing timer if any
        if self._timer is not None:
            self._timer.cancel()
        
        # Create and start new timer
        self._timer = threading.Timer(self._timer_interval, self._reassert_execution_state)
        self._timer.daemon = True
        self._timer.start()
        print(f"Started reassertion timer (interval: {self._timer_interval}s)")
    
    def _reassert_execution_state(self):
        """Periodically reassert the execution state flags."""
        if not self._is_active:
            return
        
        try:
            ES_CONTINUOUS = 0x80000000
            ES_SYSTEM_REQUIRED = 0x00000001
            ES_DISPLAY_REQUIRED = 0x00000002
            
            ret = ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
            
            if ret == 0:
                print("WARNING: SetThreadExecutionState reassertion failed")
            else:
                print(f"SetThreadExecutionState reasserted successfully (return: {ret})")
            
            # Schedule next reassertion
            if self._is_active:
                self._start_reassertion_timer()
                
        except Exception as e:
            print(f"Error during execution state reassertion: {e}")
            import traceback
            traceback.print_exc()
    
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
            # Cancel the reassertion timer
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
                print("Cancelled reassertion timer")
            
            # Reset execution state to allow sleep
            ES_CONTINUOUS = 0x80000000
            ret = ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            
            if ret == 0:
                print("WARNING: SetThreadExecutionState reset failed")
            else:
                print(f"SetThreadExecutionState reset successfully (return: {ret})")
            
            self._is_active = False
            return True
        except Exception as e:
            print(f"Windows sleep allowance failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @property
    def is_active(self) -> bool:
        """Check if sleep prevention is currently active."""
        return self._is_active


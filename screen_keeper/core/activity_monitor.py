"""
Activity monitoring module.
Detects mouse and keyboard inactivity.
"""

import time
import threading
from typing import Callable, Optional
from pynput import mouse, keyboard


class ActivityMonitor:
    """Monitors mouse and keyboard activity."""
    
    def __init__(self, inactivity_timeout: float = 60.0):
        """
        Initialize activity monitor.
        
        Args:
            inactivity_timeout: Time in seconds before considering user inactive
        """
        self.inactivity_timeout = inactivity_timeout
        self.last_activity_time = time.time()
        self._is_monitoring = False
        self._mouse_listener: Optional[mouse.Listener] = None
        self._keyboard_listener: Optional[keyboard.Listener] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._on_inactive_callback: Optional[Callable[[], None]] = None
        self._on_active_callback: Optional[Callable[[], None]] = None
        self._is_inactive = False
        
    def set_inactivity_callback(self, callback: Callable[[], None]) -> None:
        """Set callback to be called when user becomes inactive."""
        self._on_inactive_callback = callback
    
    def set_activity_callback(self, callback: Callable[[], None]) -> None:
        """Set callback to be called when user becomes active."""
        self._on_active_callback = callback
    
    def _on_mouse_move(self, x: int, y: int) -> None:
        """Handle mouse movement."""
        self._update_activity()
    
    def _on_mouse_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        """Handle mouse click."""
        self._update_activity()
    
    def _on_key_press(self, key: keyboard.Key) -> None:
        """Handle key press."""
        self._update_activity()
    
    def _update_activity(self) -> None:
        """Update last activity time."""
        was_inactive = self._is_inactive
        self.last_activity_time = time.time()
        
        if was_inactive:
            self._is_inactive = False
            if self._on_active_callback:
                self._on_active_callback()
    
    def _monitor_loop(self) -> None:
        """Monitor inactivity in a separate thread."""
        while self._is_monitoring:
            time.sleep(1.0)  # Check every second
            
            time_since_activity = time.time() - self.last_activity_time
            
            if time_since_activity >= self.inactivity_timeout:
                if not self._is_inactive:
                    self._is_inactive = True
                    if self._on_inactive_callback:
                        self._on_inactive_callback()
            else:
                if self._is_inactive:
                    self._is_inactive = False
                    if self._on_active_callback:
                        self._on_active_callback()
    
    def start(self) -> bool:
        """Start monitoring activity."""
        if self._is_monitoring:
            return False
        
        try:
            self.last_activity_time = time.time()
            self._is_monitoring = True
            
            # Start mouse listener
            self._mouse_listener = mouse.Listener(
                on_move=self._on_mouse_move,
                on_click=self._on_mouse_click
            )
            self._mouse_listener.start()
            
            # Start keyboard listener
            self._keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press
            )
            self._keyboard_listener.start()
            
            # Start monitoring thread
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            
            return True
        except Exception as e:
            print(f"Error starting activity monitor: {e}")
            self._is_monitoring = False
            return False
    
    def stop(self) -> bool:
        """Stop monitoring activity."""
        if not self._is_monitoring:
            return False
        
        self._is_monitoring = False
        
        try:
            if self._mouse_listener:
                self._mouse_listener.stop()
            if self._keyboard_listener:
                self._keyboard_listener.stop()
            if self._monitor_thread:
                self._monitor_thread.join(timeout=2.0)
        except Exception as e:
            print(f"Error stopping activity monitor: {e}")
        
        return True
    
    def set_timeout(self, timeout: float) -> None:
        """Update inactivity timeout."""
        self.inactivity_timeout = timeout
    
    @property
    def is_inactive(self) -> bool:
        """Check if user is currently inactive."""
        return self._is_inactive
    
    @property
    def time_since_activity(self) -> float:
        """Get time in seconds since last activity."""
        return time.time() - self.last_activity_time


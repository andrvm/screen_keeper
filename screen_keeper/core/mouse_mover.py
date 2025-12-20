"""
Mouse movement module.
Moves mouse cursor to prevent screen from turning off.
"""

import time
import threading
import random
from typing import Optional
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key


class MouseMover:
    """Moves mouse cursor and/or simulates keyboard input to keep screen alive."""
    
    # Simulation modes
    MODE_MOUSE = "mouse"
    MODE_KEYBOARD = "keyboard"
    MODE_BOTH = "both"
    
    def __init__(self, interval: float = 30.0, movement_distance: int = 1, mode: str = MODE_BOTH):
        """
        Initialize activity simulator.
        
        Args:
            interval: Time in seconds between activity simulations
            movement_distance: Distance in pixels to move mouse (default: 1 pixel)
            mode: Simulation mode - "mouse", "keyboard", or "both" (default: "both")
        """
        self.interval = interval
        self.movement_distance = movement_distance
        self.mode = mode
        self._is_running = False
        self._thread: Optional[threading.Thread] = None
        self._mouse = MouseController()
        self._keyboard = KeyboardController()
        self._original_position: Optional[tuple] = None
        
    def start(self) -> bool:
        """Start simulating activity periodically."""
        if self._is_running:
            return False
        
        try:
            self._is_running = True
            self._original_position = self._mouse.position
            self._thread = threading.Thread(target=self._activity_loop, daemon=True)
            self._thread.start()
            print(f"Activity simulator started (mode: {self.mode})")
            return True
        except Exception as e:
            print(f"Error starting activity simulator: {e}")
            self._is_running = False
            return False
    
    def stop(self) -> bool:
        """Stop simulating activity."""
        if not self._is_running:
            return False
        
        self._is_running = False
        
        try:
            if self._thread:
                self._thread.join(timeout=2.0)
            
            # Return mouse to original position if possible
            if self._original_position and self.mode in [self.MODE_MOUSE, self.MODE_BOTH]:
                try:
                    self._mouse.position = self._original_position
                except:
                    pass
        except Exception as e:
            print(f"Error stopping activity simulator: {e}")
        
        print("Activity simulator stopped")
        return True
    
    def _activity_loop(self) -> None:
        """Main loop that simulates activity periodically."""
        while self._is_running:
            time.sleep(self.interval)
            
            if not self._is_running:
                break
            
            try:
                # Simulate activity based on mode
                if self.mode in [self.MODE_KEYBOARD, self.MODE_BOTH]:
                    self._simulate_keyboard()
                
                if self.mode in [self.MODE_MOUSE, self.MODE_BOTH]:
                    self._simulate_mouse()
                    
            except Exception as e:
                print(f"Error simulating activity: {e}")
    
    def _simulate_keyboard(self) -> None:
        """
        Simulate keyboard activity by toggling Scroll Lock.
        This is detected as real activity by security software like SecretNet.
        """
        try:
            # Toggle Scroll Lock twice (on then off) to return to original state
            self._keyboard.press(Key.scroll_lock)
            self._keyboard.release(Key.scroll_lock)
            time.sleep(0.1)
            self._keyboard.press(Key.scroll_lock)
            self._keyboard.release(Key.scroll_lock)
            print("Keyboard activity simulated (Scroll Lock toggled)")
        except Exception as e:
            print(f"Error simulating keyboard activity: {e}")
    
    def _simulate_mouse(self) -> None:
        """
        Simulate mouse activity by moving cursor slightly.
        This prevents screen timeout but is barely noticeable.
        """
        try:
            current_pos = self._mouse.position
            
            # Move mouse by a small amount (1 pixel)
            # This is enough to prevent screen timeout but barely noticeable
            new_x = current_pos[0] + random.choice([-self.movement_distance, self.movement_distance])
            new_y = current_pos[1] + random.choice([-self.movement_distance, self.movement_distance])
            
            self._mouse.position = (new_x, new_y)
            
            # Move back immediately to original position
            time.sleep(0.1)
            self._mouse.position = current_pos
            print("Mouse activity simulated (1 pixel movement)")
            
        except Exception as e:
            print(f"Error simulating mouse activity: {e}")
    
    def set_interval(self, interval: float) -> None:
        """Update activity simulation interval."""
        self.interval = interval
    
    def set_mode(self, mode: str) -> None:
        """
        Update simulation mode.
        
        Args:
            mode: "mouse", "keyboard", or "both"
        """
        if mode in [self.MODE_MOUSE, self.MODE_KEYBOARD, self.MODE_BOTH]:
            self.mode = mode
            print(f"Simulation mode changed to: {mode}")
        else:
            print(f"Invalid mode: {mode}. Using current mode: {self.mode}")
    
    @property
    def is_running(self) -> bool:
        """Check if activity simulator is currently running."""
        return self._is_running


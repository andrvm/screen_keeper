"""
Mouse movement module.
Moves mouse cursor to prevent screen from turning off.
"""

import time
import threading
import random
from typing import Optional
from pynput.mouse import Controller as MouseController


class MouseMover:
    """Moves mouse cursor to keep screen alive."""
    
    def __init__(self, interval: float = 30.0, movement_distance: int = 1):
        """
        Initialize mouse mover.
        
        Args:
            interval: Time in seconds between movements
            movement_distance: Distance in pixels to move (default: 1 pixel)
        """
        self.interval = interval
        self.movement_distance = movement_distance
        self._is_running = False
        self._thread: Optional[threading.Thread] = None
        self._mouse = MouseController()
        self._original_position: Optional[tuple] = None
        
    def start(self) -> bool:
        """Start moving mouse periodically."""
        if self._is_running:
            return False
        
        try:
            self._is_running = True
            self._original_position = self._mouse.position
            self._thread = threading.Thread(target=self._move_loop, daemon=True)
            self._thread.start()
            return True
        except Exception as e:
            print(f"Error starting mouse mover: {e}")
            self._is_running = False
            return False
    
    def stop(self) -> bool:
        """Stop moving mouse."""
        if not self._is_running:
            return False
        
        self._is_running = False
        
        try:
            if self._thread:
                self._thread.join(timeout=2.0)
            
            # Return mouse to original position if possible
            if self._original_position:
                try:
                    self._mouse.position = self._original_position
                except:
                    pass
        except Exception as e:
            print(f"Error stopping mouse mover: {e}")
        
        return True
    
    def _move_loop(self) -> None:
        """Main loop that moves mouse periodically."""
        while self._is_running:
            time.sleep(self.interval)
            
            if not self._is_running:
                break
            
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
                
            except Exception as e:
                print(f"Error moving mouse: {e}")
    
    def set_interval(self, interval: float) -> None:
        """Update movement interval."""
        self.interval = interval
    
    @property
    def is_running(self) -> bool:
        """Check if mouse mover is currently running."""
        return self._is_running


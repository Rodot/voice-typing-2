"""Text typing for emulating keyboard input."""

import time

from pynput.keyboard import Controller


class TextTyper:
    """Manages text input through keyboard emulation"""

    def __init__(self) -> None:
        """Initialize with keyboard controller"""
        self.keyboard = Controller()

    def type(self, text: str, delay: float = 0.01) -> None:
        """Type text using keyboard emulation"""
        for char in text:
            time.sleep(delay)
            self.keyboard.type(char)

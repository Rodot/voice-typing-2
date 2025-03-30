"""Text input management for emulating keyboard typing."""

import time

from pynput.keyboard import Controller, Key


class TextInputManager:
    """Manages text input through keyboard emulation"""

    def __init__(self) -> None:
        """Initialize with keyboard controller"""
        self.keyboard = Controller()

    def type_text(self, text: str, delay: float = 0.01) -> None:
        """Type text using keyboard emulation with correct layout"""
        for char in text:
            time.sleep(delay)
            self.keyboard.type(char)

    def erase_text(self, text: str, delay: float = 0.01) -> None:
        """Erase text using keyboard backspace"""
        for _ in range(len(text)):
            time.sleep(delay)
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)

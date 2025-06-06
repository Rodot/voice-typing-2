"""Text typing for emulating keyboard input."""

import time

from pynput.keyboard import Controller, Key


class TextTyper:
    """Manages text input through keyboard emulation"""

    def __init__(self) -> None:
        """Initialize with keyboard controller"""
        self.keyboard = Controller()

    def type(self, text: str) -> None:
        """Type text using keyboard emulation"""
        self.keyboard.type(text)

    def erase(self, text: str) -> None:
        """Erase text using keyboard emulation"""
        for _char in text:
            time.sleep(0.01)
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)

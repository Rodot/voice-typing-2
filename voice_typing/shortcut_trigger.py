"""Shortcut event management for voice typing."""

import logging
from collections.abc import Callable

import pynput.keyboard
from pynput.keyboard import Key, KeyCode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ShortcutTrigger:
    """Manages keyboard shortcuts for triggering voice recording"""

    def __init__(
        self,
        on_shortcut_press: Callable[[str], None],
        on_shortcut_release: Callable[[str], None],
    ) -> None:
        self.shortcuts: dict[frozenset, str] = {
            frozenset([Key.alt_l, Key.f2]): "en",
            frozenset([Key.alt_l, Key.f3]): "fr",
        }

        self.on_shortcut_press = on_shortcut_press
        self.on_shortcut_release = on_shortcut_release
        self.currently_pressed_keys: set = set()
        self.active_command: str | None = None
        self.active_shortcut: frozenset | None = None
        self.listener: pynput.keyboard.Listener | None = None

    def start_listening(self) -> pynput.keyboard.Listener:
        self.listener = pynput.keyboard.Listener(
            on_press=self._on_key_press, on_release=self._on_key_release
        )
        self.listener.start()
        return self.listener

    def stop_listening(self) -> None:
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _on_key_press(self, key: Key | KeyCode | None) -> None:
        if key is None:
            return
        self.currently_pressed_keys.add(key)

        if self.active_command is not None:
            return

        pressed_keys = frozenset(self.currently_pressed_keys)
        for shortcut, command in self.shortcuts.items():
            if shortcut.issubset(pressed_keys) and len(shortcut) > 0:
                self.active_command = command
                self.on_shortcut_press(command)
                break

    def _on_key_release(self, _key: Key | KeyCode | None) -> None:
        if self.active_command is not None:
            self.on_shortcut_release(self.active_command)
            self.currently_pressed_keys.clear()
            self.active_command = None

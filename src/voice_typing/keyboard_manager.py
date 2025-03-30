"""Keyboard event management for voice typing."""

from collections.abc import Callable

import pynput.keyboard
from pynput.keyboard import Key


class KeyboardManager:
    """Manages keyboard events for triggering voice recording"""

    def __init__(
        self,
        on_recording_start: Callable[[], None],
        on_recording_stop: Callable[[], None],
    ) -> None:
        """Initialize keyboard manager with trigger keys and callbacks"""
        self.trigger_keys: set[Key] = {Key.alt, Key.ctrl, Key.cmd}
        self.on_recording_start = on_recording_start
        self.on_recording_stop = on_recording_stop
        self.currently_pressed_keys: set[Key] = set()
        self.recording = False
        self.processing = False
        self.listener: pynput.keyboard.Listener | None = None

    def start_listening(self) -> pynput.keyboard.Listener:
        """Start listening for keyboard events"""
        self.listener = pynput.keyboard.Listener(
            on_press=self._on_key_press, on_release=self._on_key_release
        )
        self.listener.start()
        return self.listener

    def stop_listening(self) -> None:
        """Stop listening for keyboard events"""
        if self.listener:
            self.listener.stop()
            self.listener = None

    def set_processing(self, *, is_processing: bool) -> None:
        """Set processing state"""
        self.processing = is_processing

    def _on_key_press(self, key: pynput.keyboard.Key) -> None:
        """Handle key press events"""
        self.currently_pressed_keys.add(key)
        if (
            self.trigger_keys.issubset(self.currently_pressed_keys)
            and not self.recording
            and not self.processing
        ):
            self.recording = True
            self.on_recording_start()

    def _on_key_release(self, key: pynput.keyboard.Key) -> None:
        """Handle key release events"""
        if key not in self.currently_pressed_keys:
            return
        self.currently_pressed_keys.remove(key)
        if (
            self.recording
            and key in self.trigger_keys
            and not any(k in self.currently_pressed_keys for k in self.trigger_keys)
        ):
            self.recording = False
            self.on_recording_stop()

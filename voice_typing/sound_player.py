"""Sound playback functionality for voice typing."""

import logging
from pathlib import Path
from typing import Any, Final

import sounddevice as sd
import soundfile as sf

logger = logging.getLogger(__name__)


class SoundPlayer:
    """Handles sound loading and playback with lazy loading"""

    ASSETS_DIR: Final[Path] = Path(__file__).parent / "assets"

    def __init__(self) -> None:
        """Initialize the sound player"""
        self.sounds: dict[str, dict[str, Any]] = {}

    def _load_sound(self, sound_name: str) -> bool:
        """Load a sound file into memory"""
        try:
            sound_path = self.ASSETS_DIR / sound_name
            data, sample_rate = sf.read(sound_path)
            self.sounds[sound_name] = {"data": data, "sample_rate": sample_rate}
        except (FileNotFoundError, sf.SoundFileError):
            logger.exception("Failed to load sound %s", sound_name)
            return False
        return True

    def play(self, sound_name: str) -> None:
        """Play a sound, loading it first if not already loaded"""
        if sound_name not in self.sounds and not self._load_sound(sound_name):
            return

        sound = self.sounds[sound_name]
        sd.play(sound["data"], sound["sample_rate"])

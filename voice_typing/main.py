"""Main application module for voice typing."""

import logging
import os
import tempfile
import time
from typing import Final

import requests

from voice_typing.audio_recorder import AudioRecorder
from voice_typing.shortcut_trigger import ShortcutTrigger
from voice_typing.text_typer import TextTyper
from voice_typing.whisper_client import HttpWhisperClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class VoiceTypingApp:
    """Main application class for voice typing."""

    WHISPER_URL: Final[str] = "http://localhost:9000"
    SAMPLE_RATE: Final[int] = 16000

    def __init__(self) -> None:
        """Initialize the voice typing application."""
        self.audio_recorder = AudioRecorder(sample_rate=self.SAMPLE_RATE)
        self.text_input = TextTyper()
        self.whisper_client = HttpWhisperClient(base_url=self.WHISPER_URL)
        self.shortcut_manager = ShortcutTrigger(
            on_recording_start=self.start_recording,
            on_recording_stop=self.stop_recording,
        )

    def start(self) -> None:
        """Start the voice typing application."""
        while not self.whisper_client.health_check():
            logger.info("Waiting for Whisper API to be available...")
            time.sleep(3)
        logger.info("Voice Typing started. Press Alt+Ctrl+Cmd to record.")
        self.shortcut_manager.start_listening()
        try:
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            logger.info("Shutting down Voice Typing...")
        finally:
            self.shortcut_manager.stop_listening()

    def start_recording(self) -> None:
        """Start recording audio."""
        self.audio_recorder.start_recording()

    def stop_recording(self) -> None:
        """Stop recording and process the audio."""
        self.audio_recorder.stop_recording()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name

        if self.audio_recorder.save_to_file(temp_path):
            try:
                transcript = self.whisper_client.transcribe(temp_path)
                cleaned_text = self._clean_transcript(transcript)
                if cleaned_text:
                    logger.info("Typing: %s", cleaned_text)
                    self.text_input.type_text(cleaned_text)
                else:
                    logger.info("No text detected")
            except requests.RequestException:
                logger.exception("Error during transcription request")
            except OSError:
                logger.exception("Error handling audio file")
            finally:
                os.unlink(temp_path)
        else:
            logger.info("No audio recorded")

    def _clean_transcript(self, transcript: str) -> str:
        """Clean the transcript by removing extra whitespace and line breaks."""
        cleaned = transcript.strip()
        cleaned = cleaned.replace("\n", " ")
        return " ".join(cleaned.split())


def main() -> None:
    """Run the voice typing application."""
    app = VoiceTypingApp()
    app.start()


if __name__ == "__main__":
    main()

import logging
import os
import tempfile
import time
from typing import Final

from voice_typing.audio_recorder import AudioRecorder
from voice_typing.shortcut_trigger import ShortcutTrigger
from voice_typing.sound_player import SoundPlayer
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
        self.audio_recorder = AudioRecorder(sample_rate=self.SAMPLE_RATE)
        self.text_typer = TextTyper()
        self.whisper_client = HttpWhisperClient(base_url=self.WHISPER_URL)
        self.sound_player = SoundPlayer()
        self.shortcut_trigger = ShortcutTrigger(
            on_shortcut_press=self.start_recording,
            on_shortcut_release=self.stop_recording_process_and_type,
        )

    def start(self) -> None:
        while not self.whisper_client.health_check():
            logger.info("Waiting for Whisper API...")
            time.sleep(3)
        logger.info("Voice Typing started.")
        logger.info("Press Shift+F1 for English, Shift+F2 for French")
        self.shortcut_trigger.start_listening()
        try:
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            logger.info("Shutting down Voice Typing...")
        finally:
            self.shortcut_trigger.stop_listening()

    def start_recording(self, command: str) -> None:
        logger.info("Recording %s", command)
        self.sound_player.play("start_recording.wav")
        self.audio_recorder.start_recording()

    def stop_recording_process_and_type(self, command: str) -> None:
        self.sound_player.play("stop_recording.wav")
        try:
            self.audio_recorder.stop_recording()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                self.audio_recorder.save_to_file(temp_path)
                transcript = self.whisper_client.transcribe(temp_path, command)
                transcript = self._clean_transcript(transcript)
        finally:
            os.unlink(temp_path)
        logger.info("Typing: %s", transcript)
        self.text_typer.type(transcript)

    def _clean_transcript(self, transcript: str) -> str:
        cleaned = transcript.strip()
        cleaned = cleaned.replace("\n", " ")
        return " ".join(cleaned.split())


def main() -> None:
    app = VoiceTypingApp()
    app.start()


if __name__ == "__main__":
    main()

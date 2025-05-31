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
        self.state = "idle"
        self.next_state = "idle"
        self.language = "end"
        self.shortcut_trigger = ShortcutTrigger(
            on_shortcut_press=self.on_start_record,
            on_shortcut_release=self.on_stop_record,
        )

    def start(self) -> None:
        while not self.whisper_client.health_check():
            logger.info("Waiting for Whisper API...")
            time.sleep(3)
        logger.info("Whisper ready, loading model...")
        self.whisper_client.transcribe("./voice_typing/assets/jfk.wav")
        logger.info(
            "Voice typing: Press and hold Shift+F1 for English, Shift+F2 for French"
        )
        self.sound_player.play("start_recording.wav")
        self.sound_player.play("stop_recording.wav")
        self.shortcut_trigger.start_listening()
        try:
            while True:
                self.update()
                time.sleep(0.2)
        finally:
            logger.info("Shutting down Voice Typing...")
            self.shortcut_trigger.stop_listening()

    def update(self) -> None:
        if self.state == "idle" and self.next_state == "idle":
            return
        if self.state == "idle" and self.next_state == "recording":
            self.state = "recording"
            self.start_recording("en")
        elif self.state == "recording" and self.next_state == "idle":
            self.stop_recording_process_and_type()
            self.state = "idle"

    def on_start_record(self, language: str) -> None:
        if self.state == "idle" and self.next_state == "idle":
            self.next_state = "recording"
            self.language = language

    def on_stop_record(self, command: str) -> None:
        self.next_state = "idle"

    def start_recording(self, command: str) -> None:
        self.sound_player.play("start_recording.wav")
        self.audio_recorder.start_recording()

    def stop_recording_process_and_type(self) -> None:
        if not self.audio_recorder.recording:
            return
        self.sound_player.play("stop_recording.wav")
        try:
            self.audio_recorder.stop_recording()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                self.audio_recorder.save_to_file(temp_path)
                transcript = self.whisper_client.transcribe(temp_path, self.language)
                transcript = self._clean_transcript(transcript)
                logger.info("[%s] %s", self.language, transcript)
                self.text_typer.type(transcript)
        except Exception:
            logger.exception("Error during transcription")
        finally:
            os.unlink(temp_path)

    def _clean_transcript(self, transcript: str) -> str:
        cleaned = transcript.strip()
        return " ".join(cleaned.split())


def main() -> None:
    app = VoiceTypingApp()
    app.start()


if __name__ == "__main__":
    main()

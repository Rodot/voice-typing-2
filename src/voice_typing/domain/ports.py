"""Domain interfaces (ports) for voice typing."""

from typing import Protocol

from voice_typing.domain.models import AudioData, TranscriptionResult


class WhisperClient(Protocol):
    """Interface for a client that communicates with the Whisper API."""

    def transcribe(self, audio_data: AudioData) -> TranscriptionResult:
        """Transcribe audio data to text.

        Args:
            audio_data: The audio data to transcribe

        Returns:
            The transcription result
        """


class TranscriptionService(Protocol):
    """Interface for a service that transcribes audio to text."""

    def transcribe(self, audio_data: AudioData) -> TranscriptionResult:
        """Transcribe audio data to text.

        Args:
            audio_data: The audio data to transcribe

        Returns:
            The transcription result
        """

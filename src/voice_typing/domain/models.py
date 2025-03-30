"""Domain models for voice typing."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AudioData:
    """Audio data for transcription."""

    file_path: str

    @classmethod
    def from_file(cls, file_path: str) -> "AudioData":
        """Create AudioData from a WAV file.

        Args:
            file_path: Path to the WAV file

        Returns:
            AudioData instance with the file path
        """
        path = Path(file_path)
        return cls(file_path=str(path))


@dataclass(frozen=True)
class TranscriptionResult:
    """Result of a transcription operation."""

    text: str

    @property
    def has_content(self) -> bool:
        """Check if the transcription has content.

        Returns:
            True if the transcription has content, False otherwise
        """
        return bool(self.text)

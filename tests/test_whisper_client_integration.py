"""Integration tests for the HTTP Whisper client."""

from voice_typing.domain.models import AudioData
from voice_typing.infrastructure.whisper_client import HttpWhisperClient


def test_transcribe_jfk_speech() -> None:
    """Test transcription of JFK's speech using the actual Whisper service.

    This test requires the Whisper service to be running on localhost:9000.
    """
    # Load JFK sample speech audio data
    audio_data = AudioData.from_file("./tests/samples/jfk.wav")

    # Create an HttpWhisperClient configured for the local Whisper service
    whisper_client = HttpWhisperClient(base_url="http://localhost:9000")

    # Perform transcription
    result = whisper_client.transcribe(audio_data)

    # Check that we got a non-empty result
    assert result.has_content

    # Check for key phrase in JFK's famous quote
    assert "ask not what your country can do for you" in result.text.lower()

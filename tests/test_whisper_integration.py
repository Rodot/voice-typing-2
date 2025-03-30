"""Integration tests for the HTTP Whisper client."""

from voice_typing.whisper_client import HttpWhisperClient


def test_transcribe_jfk_speech() -> None:
    """Test transcription of JFK's speech using the actual Whisper service.
    This test requires the Whisper service to be running on localhost:9000.
    """
    audio_path = "./tests/samples/jfk.wav"
    whisper_client = HttpWhisperClient(base_url="http://localhost:9000")
    result = whisper_client.transcribe(audio_path)
    assert "ask not what your country can do for you" in result.lower()

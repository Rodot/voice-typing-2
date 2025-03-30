"""HTTP client for the Whisper ASR API."""

import os
from dataclasses import dataclass

import requests

from voice_typing.domain.models import AudioData, TranscriptionResult


@dataclass
class HttpWhisperClient:
    """Client for the Whisper ASR API using HTTP.

    This client communicates with the Whisper ASR API to transcribe audio data.
    It's configured to work with the onerahmet/openai-whisper-asr-webservice.
    """

    base_url: str

    def transcribe(self, audio_data: AudioData) -> TranscriptionResult:
        """Transcribe audio data by sending it to the Whisper API.

        Args:
            audio_data: The audio data file path to transcribe

        Returns:
            The transcription result

        Raises:
            requests.RequestException: If the API request fails
        """
        # Prepare the API endpoint
        endpoint = f"{self.base_url}/asr"

        # Get the filename from the path
        filename = os.path.basename(audio_data.file_path)

        # Open the audio file for reading
        with open(audio_data.file_path, "rb") as audio_file:
            # Set up multipart form data with the audio file
            files = {"audio_file": (filename, audio_file, "audio/wav")}

            # Set query parameters according to the API documentation
            params = {"encode": "true", "task": "transcribe", "output": "txt"}

            # Make the API request
            response = requests.post(endpoint, files=files, params=params, timeout=30)

            # Check for errors
            response.raise_for_status()

            # Extract the transcription text
            transcription_text = response.text

            # Return the result
            return TranscriptionResult(text=transcription_text)

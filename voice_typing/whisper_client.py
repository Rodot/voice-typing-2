"""HTTP client for the Whisper ASR API."""

from dataclasses import dataclass

import requests


@dataclass
class HttpWhisperClient:
    """Client for the Whisper ASR API using HTTP"""

    base_url: str

    def transcribe(self, audio_path: str, language: str = "en") -> str:
        endpoint = f"{self.base_url}/asr"

        with open(audio_path, "rb") as audio_file:
            files = {"audio_file": (audio_path, audio_file, "audio/wav")}
            params = {
                "encode": "true",
                "task": "transcribe",
                "output": "txt",
                "language": language,
            }
            response = requests.post(endpoint, files=files, params=params, timeout=30)
            response.raise_for_status()
            return response.text

    def health_check(self) -> bool:
        endpoint = f"{self.base_url}/docs"
        try:
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return False
        return True

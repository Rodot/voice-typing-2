"""Audio recording functionality for voice typing."""

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    """Records audio from the microphone"""

    def __init__(self, sample_rate: int) -> None:
        """Initialize the audio recorder"""
        self.sample_rate = sample_rate
        self.frames: list[np.ndarray] = []
        self.stream: sd.InputStream | None = None
        self.recording = False

    def start_recording(self) -> None:
        """Start recording audio from microphone"""
        self.recording = True
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate, channels=1, callback=self._audio_callback
        )
        self.stream.start()

    def stop_recording(self) -> None:
        """Stop recording audio"""
        self.recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def save_to_file(self, file_path: str) -> bool:
        """Save recorded audio to a file"""
        if not self.frames:
            return False

        audio_data = np.concatenate(self.frames, axis=0)
        sf.write(file_path, audio_data, self.sample_rate)
        return True

    def _audio_callback(
        self,
        indata: np.ndarray,
        _frame_count: int,
        _time_info: dict,
        _status: sd.CallbackFlags,
    ) -> None:
        """Callback for audio recording"""
        if self.recording:
            self.frames.append(indata.copy())

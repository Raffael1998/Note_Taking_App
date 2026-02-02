from __future__ import annotations

import os
from threading import Event, Thread
from typing import List

try:
    import sounddevice as sd  # type: ignore
    import soundfile as sf  # type: ignore
except Exception:  # pragma: no cover - optional dependency may be missing
    sd = None
    sf = None

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


class VoiceRecorder:
    """Record audio from the microphone and convert it to text."""

    def __init__(self, save_path: str = "last_recording.wav", language: str = "fr-FR") -> None:
        self.save_path = save_path
        self.language = language
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
        self._sd_available = sd is not None and sf is not None

    def _record_audio(self) -> None:
        """Record audio until the user presses Enter to stop."""
        if not self._sd_available:
            raise RuntimeError("Audio recording is not available (PortAudio missing)")

        print("Recording... press Enter to stop.")
        stop_event = Event()
        audio_frames: List[np.ndarray] = []
        samplerate = 16000

        def wait_for_stop() -> None:
            input()
            stop_event.set()

        Thread(target=wait_for_stop, daemon=True).start()

        def callback(indata: np.ndarray, frames: int, time, status) -> None:
            if status:
                print(status)
            audio_frames.append(indata.copy())
            if stop_event.is_set():
                raise sd.CallbackStop()

        assert sd is not None  # for type checkers
        assert sf is not None
        with sd.InputStream(
            channels=1,
            samplerate=samplerate,
            dtype="int16",
            callback=callback,
        ):
            while not stop_event.is_set():
                sd.sleep(100)

        if not audio_frames:
            raise RuntimeError("No audio captured")

        audio = np.concatenate(audio_frames, axis=0)
        sf.write(self.save_path, audio, samplerate)
        print(f"Audio saved to {self.save_path}")

    def record_text(self) -> str:
        """Record from the microphone and return transcribed text."""
        self._record_audio()
        try:
            with open(self.save_path, "rb") as file:
                lang = self.language.split("-")[0]
                response = self.client.audio.transcriptions.create(
                    model="whisper-1", file=file, language=lang
                )
            text = response.text.strip()
            print(f"[DEBUG] Recognized text: {text}")
            return text
        except Exception as exc:
            raise RuntimeError(f"Speech recognition failed: {exc}")

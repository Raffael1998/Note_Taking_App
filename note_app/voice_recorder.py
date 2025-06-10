from __future__ import annotations

from threading import Event, Thread
from typing import List

import os
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI


class VoiceRecorder:
    """Record audio from the microphone and convert it to text."""

    def __init__(self, save_path: str = "last_recording.wav", language: str = "fr-FR") -> None:
        self.recognizer = sr.Recognizer()
        self.save_path = save_path
        self.language = language
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

    def _record_audio(self) -> sr.AudioData:
        """Record audio until the user presses Enter to stop."""
        with sr.Microphone() as source:
            print("Calibrating ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Recording... press Enter to stop.")

            stop_event = Event()
            audio_frames: List[bytes] = []
            sample_rate = source.SAMPLE_RATE
            sample_width = source.SAMPLE_WIDTH

            def wait_for_stop() -> None:
                input()
                stop_event.set()

            Thread(target=wait_for_stop, daemon=True).start()

            while not stop_event.is_set():
                try:
                    audio = self.recognizer.listen(
                        source, timeout=1, phrase_time_limit=1
                    )
                    audio_frames.append(audio.get_raw_data())
                except sr.WaitTimeoutError:
                    pass

            if not audio_frames:
                raise RuntimeError("No audio captured")

            raw_data = b"".join(audio_frames)
            audio_data = sr.AudioData(raw_data, sample_rate, sample_width)

            with open(self.save_path, "wb") as file:
                file.write(audio_data.get_wav_data())
            print(f"Audio saved to {self.save_path}")

            return audio_data

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

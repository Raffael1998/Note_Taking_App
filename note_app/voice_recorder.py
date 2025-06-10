from __future__ import annotations

import speech_recognition as sr


class VoiceRecorder:
    """Record audio from the microphone and convert it to text."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def record_text(self) -> str:
        """Record from the default microphone and return transcribed text."""
        with sr.Microphone() as source:
            print("Please speak...")
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            raise RuntimeError(f"Speech recognition failed: {exc}")

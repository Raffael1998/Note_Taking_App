from __future__ import annotations

from threading import Event, Thread
from typing import List

import speech_recognition as sr


class VoiceRecorder:
    """Record audio from the microphone and convert it to text."""

    def __init__(self, save_path: str = "last_recording.wav") -> None:
        self.recognizer = sr.Recognizer()
        self.save_path = save_path

    def _record_audio(self) -> sr.AudioData:
        """Record audio after the user presses Enter to start and stop."""
        with sr.Microphone() as source:
            print("Calibrating ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Press Enter to start recording...")
            input()
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

            return audio_data

    def record_text(self) -> str:
        """Record from the microphone and return transcribed text."""
        audio = self._record_audio()
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            raise RuntimeError(f"Speech recognition failed: {exc}")

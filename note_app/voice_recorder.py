from __future__ import annotations

from typing import List

import speech_recognition as sr


class VoiceRecorder:
    """Record audio from the microphone and convert it to text."""

    def __init__(self, save_path: str = "latest_recording.wav") -> None:
        self.recognizer = sr.Recognizer()
        self.save_path = save_path

    def _record_audio(self) -> sr.AudioData:
        """Record audio until the user presses Enter again."""
        # The ``listen_in_background`` method internally manages the microphone
        # context, so ``sr.Microphone`` should not be wrapped in a ``with``
        # statement here. Doing so would result in nested context managers and
        # raise ``AssertionError: This audio source is already inside a context
        # manager``.
        source = sr.Microphone()

        chunks: List[sr.AudioData] = []

        def callback(_: sr.Recognizer, audio: sr.AudioData) -> None:
            chunks.append(audio)

        print("Press Enter to start recording...")
        input()
        print("Recording... press Enter to stop.")

        stop_listening = self.recognizer.listen_in_background(source, callback)
        input()
        stop_listening(wait_for_stop=False)

        if not chunks:
            raise RuntimeError("No audio captured")

        sample_rate = chunks[0].sample_rate
        sample_width = chunks[0].sample_width
        raw_data = b"".join(chunk.get_raw_data() for chunk in chunks)
        audio = sr.AudioData(raw_data, sample_rate, sample_width)

        with open(self.save_path, "wb") as f:
            f.write(audio.get_wav_data())

        return audio

    def record_text(self) -> str:
        """Record from the microphone and return transcribed text."""
        audio = self._record_audio()
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            raise RuntimeError(f"Speech recognition failed: {exc}")

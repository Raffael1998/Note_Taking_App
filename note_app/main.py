from __future__ import annotations

import argparse
from typing import Callable

from .llm_interface import LLMInterface
from .note_manager import NoteManager
from .voice_recorder import VoiceRecorder


def record_note(llm: LLMInterface, notes: NoteManager, recorder: VoiceRecorder) -> None:
    """Record a note using the microphone and store a summarized version."""
    text = recorder.record_text()
    if not text:
        print("Could not understand audio.")
        return
    summary = llm.summarize(text)
    notes.add_note(summary)
    print("Note added:", summary)


def query_notes(llm: LLMInterface, notes: NoteManager, query: str) -> None:
    """Query existing notes via the LLM."""
    note_text = notes.read_notes()
    if not note_text.strip():
        print("No notes found.")
        return
    result = llm.query_notes(note_text, query)
    print("Query result:\n", result)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-powered voice note app")
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="Record a new voice note")

    query_parser = subparsers.add_parser("query", help="Query existing notes")
    query_parser.add_argument("prompt", help="Question about your notes")

    args = parser.parse_args()

    llm = LLMInterface()
    notes = NoteManager()
    recorder = VoiceRecorder()

    commands: dict[str, Callable[..., None]] = {
        "record": lambda: record_note(llm, notes, recorder),
        "query": lambda: query_notes(llm, notes, args.prompt),
    }

    commands[args.command]()


if __name__ == "__main__":
    main()

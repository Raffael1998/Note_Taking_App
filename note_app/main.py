from __future__ import annotations

import argparse
from typing import Callable

from .llm_interface import LLMInterface
from .note_manager import NoteManager
from .voice_recorder import VoiceRecorder
from .categories import load_categories


def record_note(
    llm: LLMInterface, notes: NoteManager, recorder: VoiceRecorder
) -> None:
    """Record a note, infer its category and store a summarized version."""
    text = recorder.record_text()
    if not text:
        print("Could not understand audio.")
        return
    summary = llm.summarize(text)
    categories = load_categories()
    category = llm.infer_category(text, categories)
    notes.add_note(summary, category=category)
    print("Note added:", f"[{category}] {summary}")


def query_notes(
    llm: LLMInterface,
    notes: NoteManager,
    recorder: VoiceRecorder,
    query: str | None,
    use_voice: bool,
) -> None:
    """Query existing notes via the LLM. Uses voice input when requested."""

    if use_voice:
        query_text = recorder.record_text()
        if not query_text:
            print("Could not understand audio.")
            return
    else:
        if query is None:
            raise ValueError("Query text is required when not using voice")
        query_text = query

    note_text = notes.read_notes()
    if not note_text.strip():
        print("No notes found.")
        return
    result = llm.query_notes(note_text, query_text)
    print("Query result:\n", result)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-powered voice note app")
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="Record a new voice note")
    record_parser.add_argument(
        "--language",
        "-l",
        choices=["en", "fr"],
        default="en",
        help="Recording language: en or fr",
    )

    query_parser = subparsers.add_parser("query", help="Query existing notes")
    query_parser.add_argument(
        "prompt",
        nargs="?",
        help="Question about your notes",
    )
    query_parser.add_argument(
        "--voice",
        "-v",
        action="store_true",
        help="Speak your query instead of typing",
    )
    query_parser.add_argument(
        "--language",
        "-l",
        choices=["en", "fr"],
        default="en",
        help="Recording language: en or fr",
    )

    args = parser.parse_args()

    llm = LLMInterface()
    notes = NoteManager()
    language_code = "fr-FR" if args.language == "fr" else "en-US"
    recorder = VoiceRecorder(language=language_code)

    if args.command == "record":
        record_note(llm, notes, recorder)
    elif args.command == "query":
        if not args.voice and args.prompt is None:
            parser.error("You must provide a prompt or use --voice")
        query_notes(llm, notes, recorder, args.prompt, args.voice)


if __name__ == "__main__":
    main()

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class NoteManager:
    """Manage notes saved to a text file."""

    def __init__(self, notes_path: str | Path = "notes.txt") -> None:
        self.notes_path = Path(notes_path)
        self.notes_path.touch(exist_ok=True)

    def add_note(self, note_text: str, category: str = "General") -> None:
        """Add a note with a timestamp and category."""
        timestamp = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        with self.notes_path.open("a", encoding="utf-8") as file:
            file.write(f"{timestamp} : [{category}] {note_text}\n")

    def read_notes(self) -> str:
        """Return all notes as a single string."""
        return self.notes_path.read_text(encoding="utf-8")

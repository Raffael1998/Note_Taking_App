from __future__ import annotations

from pathlib import Path
from typing import List


def load_categories(path: str | Path = "categories.txt") -> List[str]:
    """Return non-empty categories from the given file."""
    p = Path(path)
    if not p.exists():
        return []
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]

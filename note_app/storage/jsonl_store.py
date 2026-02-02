from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from note_app.memory.schema import MemoryRecord


class JsonlStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: MemoryRecord) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(record.model_dump_json())
            handle.write("\n")

    def read_all(self) -> List[MemoryRecord]:
        if not self.path.exists():
            return []
        records: List[MemoryRecord] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                records.append(MemoryRecord.model_validate_json(line))
        return records

    def iter_records(self) -> Iterable[MemoryRecord]:
        if not self.path.exists():
            return iter(())
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                yield MemoryRecord.model_validate_json(line)

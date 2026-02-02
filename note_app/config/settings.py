from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    chroma_dir: Path
    memories_path: Path
    llm_model: str
    embedding_model: str


def load_settings() -> Settings:
    load_dotenv()
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "data"
    chroma_dir = data_dir / "chroma"
    memories_path = data_dir / "memories.jsonl"
    llm_model = os.getenv("NOTE_APP_LLM_MODEL", "gpt-4.1-mini")
    embedding_model = os.getenv("NOTE_APP_EMBEDDING_MODEL", "text-embedding-3-small")
    return Settings(
        data_dir=data_dir,
        chroma_dir=chroma_dir,
        memories_path=memories_path,
        llm_model=llm_model,
        embedding_model=embedding_model,
    )

from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def get_vector_store(embedding_model: str, persist_dir: Path) -> Chroma:
    persist_dir.mkdir(parents=True, exist_ok=True)
    embeddings = OpenAIEmbeddings(model=embedding_model)
    return Chroma(
        collection_name="note_memories",
        embedding_function=embeddings,
        persist_directory=str(persist_dir),
    )

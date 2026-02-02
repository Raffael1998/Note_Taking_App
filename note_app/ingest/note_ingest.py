from __future__ import annotations

from note_app.memory.extractor import extract_memory
from note_app.storage.jsonl_store import JsonlStore


def ingest_note(llm, vector_store, store: JsonlStore, text: str, source: str, language: str):
    memory = extract_memory(llm, text, source=source, language=language)
    metadata = {
        "id": memory.id,
        "timestamp": memory.timestamp.isoformat(),
        "category": memory.category,
        "tags": ", ".join(memory.tags),
        "entities": ", ".join(memory.entities),
        "source": memory.source,
        "language": memory.language,
        "raw_text": memory.raw_text,
    }
    ids = vector_store.add_texts([memory.summary], metadatas=[metadata])
    if hasattr(vector_store, "persist"):
        vector_store.persist()
    if ids:
        memory = memory.model_copy(update={"embedding_id": ids[0]})
    store.append(memory)
    return memory

from __future__ import annotations

from typing import List

from langchain_core.documents import Document


def search_memories(vector_store, query: str, k: int = 5) -> List[Document]:
    return vector_store.similarity_search(query, k=k)

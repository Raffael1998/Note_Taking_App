from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    id: str
    timestamp: datetime
    raw_text: str
    summary: str
    category: str
    tags: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    source: str
    language: str = "en"
    embedding_id: Optional[str] = None


class MemoryDraft(BaseModel):
    summary: str
    category: str
    tags: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)

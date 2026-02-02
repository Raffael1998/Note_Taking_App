from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from note_app.memory.schema import MemoryDraft, MemoryRecord


def build_memory_extractor(llm):
    parser = PydanticOutputParser(pydantic_object=MemoryDraft)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You extract structured memory records from user notes. "
                "Return data that matches the required JSON schema exactly.",
            ),
            (
                "human",
                "Note:\n{note}\n\n"
                "Constraints:\n"
                "- Use concise summary (max 3 sentences).\n"
                "- Choose a single category label.\n"
                "- Tags and entities should be short strings.\n\n"
                "{format_instructions}",
            ),
        ]
    )
    return prompt | llm | parser, parser


def extract_memory(llm, note_text: str, source: str, language: str) -> MemoryRecord:
    extractor, parser = build_memory_extractor(llm)
    base = MemoryRecord(
        id=str(uuid4()),
        timestamp=datetime.utcnow(),
        raw_text=note_text,
        summary="",
        category="",
        tags=[],
        entities=[],
        source=source,
        language=language,
        embedding_id=None,
    )
    parsed = extractor.invoke(
        {
            "note": note_text,
            "format_instructions": parser.get_format_instructions(),
        }
    )
    return base.model_copy(
        update={
            "summary": parsed.summary,
            "category": parsed.category,
            "tags": parsed.tags,
            "entities": parsed.entities,
        }
    )

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def build_router(llm):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a router. Decide if the user's input is a new note "
                "or a query about existing notes. Answer with exactly one word: "
                "'note' or 'query'.",
            ),
            ("human", "{text}"),
        ]
    )
    return prompt | llm | StrOutputParser()


def route_text(llm, text: str) -> str:
    router = build_router(llm)
    decision = router.invoke({"text": text}).strip().lower()
    if decision not in {"note", "query"}:
        return "note"
    return decision

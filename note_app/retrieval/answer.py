from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate


def answer_from_memories(llm, query: str, memories: list) -> str:
    context_lines = []
    for doc in memories:
        meta = doc.metadata or {}
        line = (
            f"- [{meta.get('timestamp', 'unknown')}] "
            f"{meta.get('category', 'uncategorized')}: {doc.page_content}"
        )
        context_lines.append(line)
    context = "\n".join(context_lines) if context_lines else "No relevant memories found."

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You answer user questions using the provided memory context. "
                "If the answer is not in the memories, say you couldn't find it.",
            ),
            (
                "human",
                "Question: {query}\n\nMemories:\n{context}\n\nAnswer:",
            ),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"query": query, "context": context})
    return response.content.strip()

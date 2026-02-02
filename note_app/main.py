from __future__ import annotations

import argparse

from langchain_openai import ChatOpenAI

from note_app.agents.router import route_text
from note_app.config.settings import load_settings
from note_app.ingest.note_ingest import ingest_note
from note_app.retrieval.answer import answer_from_memories
from note_app.retrieval.search import search_memories
from note_app.retrieval.vector_store import get_vector_store
from note_app.storage.jsonl_store import JsonlStore


def build_llm(model_name: str):
    return ChatOpenAI(model=model_name, temperature=0.2)


def resolve_text(text_arg: str | None, prompt: str) -> str:
    if text_arg:
        return text_arg
    return input(prompt).strip()


def handle_record(llm, vector_store, store, text: str, language: str) -> None:
    memory = ingest_note(llm, vector_store, store, text, source="text", language=language)
    print("Saved memory:")
    print(f"- summary: {memory.summary}")
    print(f"- category: {memory.category}")


def handle_query(llm, vector_store, query: str) -> None:
    docs = search_memories(vector_store, query, k=5)
    answer = answer_from_memories(llm, query, docs)
    print(answer)


def handle_auto(llm, vector_store, store, text: str, language: str) -> None:
    decision = route_text(llm, text)
    if decision == "query":
        handle_query(llm, vector_store, text)
    else:
        handle_record(llm, vector_store, store, text, language)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic note taking app")
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="Save a new note")
    record_parser.add_argument("--text", help="Note text")
    record_parser.add_argument("--language", "-l", default="en", help="Note language")
    record_parser.add_argument("--voice", action="store_true", help="(Not yet implemented)")

    query_parser = subparsers.add_parser("query", help="Query saved memories")
    query_parser.add_argument("--text", help="Query text")
    query_parser.add_argument("--voice", action="store_true", help="(Not yet implemented)")

    auto_parser = subparsers.add_parser("auto", help="LLM routes note vs query")
    auto_parser.add_argument("--text", help="Input text")
    auto_parser.add_argument("--language", "-l", default="en", help="Input language")
    auto_parser.add_argument("--voice", action="store_true", help="(Not yet implemented)")

    args = parser.parse_args()

    if args.voice:
        raise SystemExit("Voice input is not implemented in the revamp yet.")

    settings = load_settings()
    llm = build_llm(settings.llm_model)
    vector_store = get_vector_store(settings.embedding_model, settings.chroma_dir)
    store = JsonlStore(settings.memories_path)

    if args.command == "record":
        text = resolve_text(args.text, "Note: ")
        handle_record(llm, vector_store, store, text, args.language)
    elif args.command == "query":
        text = resolve_text(args.text, "Query: ")
        handle_query(llm, vector_store, text)
    elif args.command == "auto":
        text = resolve_text(args.text, "Input: ")
        handle_auto(llm, vector_store, store, text, args.language)


if __name__ == "__main__":
    main()

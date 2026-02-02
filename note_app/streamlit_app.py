from __future__ import annotations

import streamlit as st

from langchain_openai import ChatOpenAI

from note_app.agents.router import route_text
from note_app.config.settings import load_settings
from note_app.ingest.note_ingest import ingest_note
from note_app.retrieval.answer import answer_from_memories
from note_app.retrieval.search import search_memories
from note_app.retrieval.vector_store import get_vector_store
from note_app.storage.jsonl_store import JsonlStore


@st.cache_resource
def get_llm(model_name: str):
    return ChatOpenAI(model=model_name, temperature=0.2)


@st.cache_resource
def get_vector_store_cached(embedding_model: str, persist_dir):
    return get_vector_store(embedding_model, persist_dir)


def main() -> None:
    st.title("Agentic Note Taking (Revamp)")
    st.info("Text-only v1. Voice capture will be added later.")

    settings = load_settings()
    llm = get_llm(settings.llm_model)
    vector_store = get_vector_store_cached(settings.embedding_model, settings.chroma_dir)
    store = JsonlStore(settings.memories_path)

    tabs = st.tabs(["Record", "Query", "Auto-route"])

    with tabs[0]:
        note_text = st.text_area("Note text", height=150)
        language = st.selectbox("Language", ["fr", "en"])
        if st.button("Save note"):
            if not note_text.strip():
                st.warning("Please enter some text.")
            else:
                memory = ingest_note(llm, vector_store, store, note_text, "text", language)
                st.success("Saved memory.")
                st.write({"summary": memory.summary, "category": memory.category})

    with tabs[1]:
        query_text = st.text_area("Query", height=100)
        if st.button("Search"):
            if not query_text.strip():
                st.warning("Please enter a query.")
            else:
                docs = search_memories(vector_store, query_text, k=5)
                answer = answer_from_memories(llm, query_text, docs)
                st.subheader("Answer")
                st.write(answer)
                st.subheader("Matches")
                for doc in docs:
                    st.write(doc.metadata)
                    st.write(doc.page_content)

    with tabs[2]:
        input_text = st.text_area("Input", height=100)
        language = st.selectbox("Language", ["fr", "en"], key="auto_lang")
        if st.button("Route"):
            if not input_text.strip():
                st.warning("Please enter text.")
            else:
                decision = route_text(llm, input_text)
                st.write(f"Router decision: {decision}")
                if decision == "query":
                    docs = search_memories(vector_store, input_text, k=5)
                    answer = answer_from_memories(llm, input_text, docs)
                    st.subheader("Answer")
                    st.write(answer)
                else:
                    memory = ingest_note(llm, vector_store, store, input_text, "text", language)
                    st.success("Saved memory.")
                    st.write({"summary": memory.summary, "category": memory.category})


if __name__ == "__main__":
    main()

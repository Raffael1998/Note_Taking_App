import os
import sys
import tempfile
from pathlib import Path

# Ensure the project root is on the Python path when running via
# ``streamlit run note_app/streamlit_app.py``. Streamlit executes the script
# as a file which sets ``sys.path[0]`` to this directory (``note_app``),
# causing ``import note_app`` to fail. Adding the parent directory allows
# imports to succeed without requiring an installed package.
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from note_app.llm_interface import LLMInterface
from note_app.note_manager import NoteManager
from note_app.categories import load_categories
from note_app.voice_recorder import VoiceRecorder


llm = LLMInterface()
notes = NoteManager()
recorder = VoiceRecorder()

st.set_page_config(page_title="AI Note App")
st.title("AI Voice Note App")


def transcribe_audio(uploaded_file: Path | None, language: str) -> str:
    """Return transcribed text from an uploaded audio file."""
    if uploaded_file is None:
        return ""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=Path(uploaded_file.name).suffix
    ) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = Path(tmp.name)
    try:
        with open(tmp_path, "rb") as f:
            response = recorder.client.audio.transcriptions.create(
                model="whisper-1", file=f, language=language
            )
        return response.text.strip()
    finally:
        tmp_path.unlink(missing_ok=True)


record_tab, query_tab, notes_tab, categories_tab = st.tabs(
    ["Record Note", "Query Notes", "Notes", "Categories"]
)


with record_tab:
    st.header("Record a new note")
    language = st.selectbox("Language", ["en", "fr"], index=1)
    mic_audio = st.audio_input("Record audio")
    text_input = st.text_area("Or enter text")
    if st.button("Add Note"):
        if mic_audio:
            text = transcribe_audio(mic_audio, language)
        else:
            text = text_input.strip()
        if not text:
            st.error("Please provide audio or text input")
        else:
            summary = llm.summarize(text)
            category = llm.infer_category(text, load_categories())
            notes.add_note(summary, category=category)
            st.success(f"Note added: [{category}] {summary}")


with query_tab:
    st.header("Query notes")
    language = st.selectbox(
        "Language", ["en", "fr"], index=1, key="query_lang"
    )
    mic_query = st.audio_input("Record query", key="query_mic")
    query_text = st.text_input("Or type your query", key="query_text")
    if st.button("Search"):
        if mic_query:
            query = transcribe_audio(mic_query, language)
        else:
            query = query_text.strip()
        if not query:
            st.error("Please provide audio or text input")
        else:
            note_text = notes.read_notes()
            if not note_text.strip():
                st.warning("No notes found")
            else:
                result = llm.query_notes(note_text, query)
                st.text_area("Result", value=result, height=200)


with notes_tab:
    st.header("Edit notes.txt")
    content = Path("notes.txt").read_text(encoding="utf-8")
    edited = st.text_area("Notes", value=content, height=300)
    if st.button("Save Notes"):
        Path("notes.txt").write_text(
            edited.replace("\r\n", "\n"), encoding="utf-8"
        )
        st.success("Notes saved")


with categories_tab:
    st.header("Edit categories.txt")
    content = Path("categories.txt").read_text(encoding="utf-8")
    edited = st.text_area(
        "Categories", value=content, height=300, key="cat_text"
    )
    if st.button("Save Categories"):
        Path("categories.txt").write_text(
            edited.replace("\r\n", "\n"), encoding="utf-8"
        )
        st.success("Categories saved")

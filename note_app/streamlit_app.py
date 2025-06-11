import os
import sys
import tempfile
from pathlib import Path
from typing import Any

# Ensure the project root is on the Python path when running via
# ``streamlit run note_app/streamlit_app.py``. Streamlit executes the script
# as a file which sets ``sys.path[0]`` to this directory (``note_app``),
# causing ``import note_app`` to fail. Adding the parent directory allows
# imports to succeed without requiring an installed package.
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import streamlit_mic_recorder as mic

from note_app.llm_interface import LLMInterface
from note_app.note_manager import NoteManager
from note_app.categories import load_categories
from note_app.voice_recorder import VoiceRecorder


llm = LLMInterface()
notes = NoteManager()
recorder = VoiceRecorder()

st.set_page_config(page_title="AI Note App")
st.title("AI Voice Note App")

# Inject custom styles and fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f0f4f8;
        }
        button.myButton {
            border-radius: 30px;
            font-weight: 600;
            color: #fff;
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def transcribe_audio(data: Any, language: str) -> str:
    """Return transcribed text from uploaded data or raw bytes."""
    if data is None:
        return ""
    if isinstance(data, bytes):
        suffix = ".wav"
        buffer = data
    else:
        suffix = Path(data.name).suffix
        buffer = data.getbuffer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(buffer)
        tmp_path = Path(tmp.name)
    try:
        with open(tmp_path, "rb") as f:
            response = recorder.client.audio.transcriptions.create(
                model="whisper-1", file=f, language=language
            )
        return response.text.strip()
    finally:
        tmp_path.unlink(missing_ok=True)


language = st.selectbox("Language", ["en", "fr"], index=1)

st.subheader("Send a note")
note_audio = mic.mic_recorder(
    start_prompt="Click to record note",
    stop_prompt="Click again to stop and save",
    key="note_rec",
)
if note_audio:
    text = transcribe_audio(note_audio["bytes"], language)
    if text:
        summary = llm.summarize(text)
        category = llm.infer_category(text, load_categories())
        notes.add_note(summary, category=category)
        st.session_state["last_note"] = f"Note added: [{category}] {summary}"
    else:
        st.session_state["last_note"] = "Could not understand audio."
if "last_note" in st.session_state:
    st.info(st.session_state["last_note"])

st.divider()

st.subheader("Search notes")
query_audio = mic.mic_recorder(
    start_prompt="Click to record query",
    stop_prompt="Click again to search",
    key="query_rec",
)
if query_audio:
    query = transcribe_audio(query_audio["bytes"], language)
    if query:
        note_text = notes.read_notes()
        if not note_text.strip():
            st.session_state["query_result"] = "No notes found"
        else:
            result = llm.query_notes(note_text, query)
            st.session_state["query_result"] = (
                result if result.strip() else "No matching notes found"
            )
    else:
        st.session_state["query_result"] = "Could not understand audio."
if "query_result" in st.session_state:
    st.text_area("Result", value=st.session_state["query_result"], height=200)

# Color-code the microphone buttons after they are rendered
st.markdown(
    """
    <script>
    function styleButtons() {
      const btns = document.querySelectorAll('button.myButton');
      if (btns.length >= 2) {
        btns[0].style.backgroundColor = '#ff6b6b';
        btns[1].style.backgroundColor = '#1e90ff';
      } else {
        setTimeout(styleButtons, 100);
      }
    }
    styleButtons();
    </script>
    """,
    unsafe_allow_html=True,
)

with st.expander("Edit notes.txt"):
    content = Path("notes.txt").read_text(encoding="utf-8")
    edited = st.text_area("Notes", value=content, height=300, key="notes_edit")
    if st.button("Save Notes"):
        Path("notes.txt").write_text(
            edited.replace("\r\n", "\n"), encoding="utf-8"
        )
        st.success("Notes saved")

with st.expander("Edit categories.txt"):
    content = Path("categories.txt").read_text(encoding="utf-8")
    edited = st.text_area(
        "Categories", value=content, height=300, key="cat_edit"
    )
    if st.button("Save Categories"):
        Path("categories.txt").write_text(
            edited.replace("\r\n", "\n"), encoding="utf-8"
        )
        st.success("Categories saved")



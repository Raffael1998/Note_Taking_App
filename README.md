# AI Voice Note Taking App

This project is a simple Python application that records voice notes, summarizes them using an LLM (such as OpenAI's GPT), and saves the summarized notes with a timestamp. You can also query existing notes using natural language.

The application defaults to the `gpt-4.1-nano` model for all LLM calls.
When recording or querying by voice you can choose between English and French
transcription using OpenAI's Whisper API. French is used by default, but you can
override it with `--language en`.

## Revamp architecture (planned)

Goal: move to a LangChain-based, agentic pipeline that turns raw notes into
structured "memories" and supports retrieval + answer generation. We'll keep
the OpenAI API for LLM + audio (if supported).

### Core data flow

1) Capture: audio or text note comes in.
2) Transcribe (if audio): speech-to-text.
3) Classify + extract: category, entities, and key facts.
4) Summarize: turn the note into a compact "memory" record.
5) Store: persist raw note + memory + embeddings in a local store.
6) Query: user voice/text query.
7) Retrieve: semantic search + filters over memories and raw notes.
8) Respond: compose an answer grounded in retrieved memories.

### Proposed modules

- `note_app/ingest`: audio capture + transcription + preprocessing.
- `note_app/memory`: memory schema, summarization chain, and storage adapter.
- `note_app/retrieval`: embeddings, vector store, and hybrid search.
- `note_app/agents`: agent(s) that orchestrate classification, summarization,
  and query answering.
- `note_app/ui`: CLI + Streamlit (or future web API).
- `note_app/config`: model and provider configuration.

### Memory record (draft)

- `id`, `timestamp`, `raw_text`
- `summary`, `category`, `tags`, `entities`
- `source` (voice/text), `language`
- `embedding` reference (vector store id)

### Open questions

- Which agent style: LLM router that decides "new note" vs. "query" and then
  dispatches to the corresponding pipeline.
- Vector store choice: Chroma for local persistence + simple setup.
- Persistence: JSONL for memory metadata + Chroma for embeddings.

### Planned dependencies (draft)

- `langchain` (core chains + agent orchestration)
- `langchain-openai` (OpenAI LLM + embeddings)
- `langchain-community` (vector store integrations)
- `chromadb` (vector store)
- `pydantic` (memory schema)
- `python-dotenv` (config)
- (future) audio libs for voice capture/transcription

## Requirements

- Python 3.10+
- `langchain` + `langchain-openai` for LLM orchestration
- `chromadb` for local vector storage
- `python-dotenv` for loading environment variables

Install dependencies with uv:

```bash
uv sync
```

Run the app with:

```bash
uv run python -m note_app.main record
```

If installation fails for the audio libraries on Windows, grab prebuilt wheels
from [the unofficial binaries site](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
and install them with `uv pip install <wheel-filename>`.

Create a `.env` file in the project root containing your OpenAI API key:

```bash
OPENAI_API_KEY=your-key-here
```

The application will automatically load this file using `python-dotenv`.

## Usage

Record a new note (text-only v1):

```bash
uv run python -m note_app.main record
```
Categories are inferred automatically from the note text.
Recording starts immediately and you press **Enter** to stop so it won't cut you
off mid-sentence.

For English use:

```bash
uv run python -m note_app.main record --language en
```

During recording a file named `last_recording.wav` is saved in the project
directory. This contains the raw audio that is sent to the LLM, which can be
useful for debugging.

Query notes:

```bash
uv run python -m note_app.main query "What do I need to buy?"
```
The returned lines include the original timestamp and category for each note.

Auto-route (LLM decides note vs. query):

```bash
uv run python -m note_app.main auto --text "Remind me to call the dentist tomorrow"
```

Voice capture is planned but not implemented in the revamp yet.

Memories are stored in `data/memories.jsonl`, with embeddings stored in
`data/chroma/`.

The list of possible categories is not fixed in v1; the LLM assigns categories
dynamically.

## Web Interface

You can run a simple web interface using **Streamlit**:

```bash
uv run streamlit run note_app/streamlit_app.py
```

Open the provided URL in your browser. The interface offers tabs to record new
notes, query existing ones, or auto-route inputs.

## Testing the OpenAI API

You can verify your API key and connectivity by running:

```bash
uv run python openai_test.py
```

This script makes a simple request to OpenAI and prints the response.

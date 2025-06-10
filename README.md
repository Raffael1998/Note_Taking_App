# AI Voice Note Taking App

This project is a simple Python application that records voice notes, summarizes them using an LLM (such as OpenAI's GPT), and saves the summarized notes with a timestamp. You can also query existing notes using natural language.

## Requirements

- Python 3.10+
- `openai` for interacting with the LLM
- `speechrecognition` for voice input

Install dependencies with:

```bash
pip install .
```

Set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY=your-key-here
```

## Usage

Record a new voice note:

```bash
python -m note_app.main record
```

Query notes:

```bash
python -m note_app.main query "What do I need to buy?"
```

Notes are stored in `notes.txt` in the project directory.

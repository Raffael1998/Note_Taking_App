# AI Voice Note Taking App

This project is a simple Python application that records voice notes, summarizes them using an LLM (such as OpenAI's GPT), and saves the summarized notes with a timestamp. You can also query existing notes using natural language.

## Requirements

- Python 3.10+
- `openai` for interacting with the LLM
- `speechrecognition` for voice input
- `python-dotenv` for loading environment variables

Install dependencies with:

```bash
pip install .
```

The `pip install` command will create `build/` and `*.egg-info` folders. These
are ignored by Git via `.gitignore` and can be safely deleted if desired.

Create a `.env` file in the project root containing your OpenAI API key:

```bash
OPENAI_API_KEY=your-key-here
```

The application will automatically load this file using `python-dotenv`.

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

## Testing the OpenAI API

You can verify your API key and connectivity by running:

```bash
python openai_test.py
```

This script makes a simple request to OpenAI and prints the response.

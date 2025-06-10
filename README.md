# AI Voice Note Taking App

This project is a simple Python application that records voice notes, summarizes them using an LLM (such as OpenAI's GPT), and saves the summarized notes with a timestamp. You can also query existing notes using natural language.

The application defaults to the `gpt-4.1-nano` model for all LLM calls.
When recording or querying by voice you can choose between English and French
speech recognition. Use the `--language` option with either `en` (default) or
`fr`.

## Requirements

- Python 3.10+
- `openai` for interacting with the LLM
- `speechrecognition` for voice input
- `pyaudio` for microphone access
- `python-dotenv` for loading environment variables

Install dependencies with:

```bash
pip install .
```

If the installation fails on Windows, download a prebuilt PyAudio wheel from
[the unofficial binaries site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
and install it with `pip install <wheel-filename>`.

The `pip install` command will create `build/` and `*.egg-info` folders. These
are ignored by Git via `.gitignore` and can be safely deleted if desired.

Create a `.env` file in the project root containing your OpenAI API key:

```bash
OPENAI_API_KEY=your-key-here
```

The application will automatically load this file using `python-dotenv`.

## Usage

Record a new voice note (English):

```bash
python -m note_app.main record
```
The recorder now waits for you to press **Enter** to start and again to stop,
so it won't cut you off mid-sentence.

For French use:

```bash
python -m note_app.main record --language fr
```

During recording a file named `last_recording.wav` is saved in the project
directory. This contains the raw audio that is sent to the LLM, which can be
useful for debugging.

Query notes:

```bash
python -m note_app.main query "What do I need to buy?"
```

You can also speak the query instead of typing:

```bash
python -m note_app.main query --voice
```

As with recording, add `--language fr` to recognise French speech.

Notes are stored in `notes.txt` in the project directory.

## Testing the OpenAI API

You can verify your API key and connectivity by running:

```bash
python openai_test.py
```

This script makes a simple request to OpenAI and prints the response.

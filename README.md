# AI Voice Note Taking App

This project is a simple Python application that records voice notes, summarizes them using an LLM (such as OpenAI's GPT), and saves the summarized notes with a timestamp. You can also query existing notes using natural language.

The application defaults to the `gpt-4.1-nano` model for all LLM calls.
When recording or querying by voice you can choose between English and French
transcription using OpenAI's Whisper API. Use the `--language` option with
either `en` (default) or `fr`.

## Requirements

- Python 3.10+
 - `openai` for interacting with the LLM and transcribing audio
 - `speechrecognition` for microphone input
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
Categories are inferred automatically from the note text.
Recording starts immediately and you press **Enter** to stop so it won't cut you
off mid-sentence.

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
The returned lines include the original timestamp and category for each note.

You can also speak the query instead of typing:

```bash
python -m note_app.main query --voice
```

As with recording, add `--language fr` to recognise French speech.

Notes are stored in `notes.txt` in the project directory.

The list of possible categories is read from `categories.txt`. Edit this file to
control how your notes are classified.

## Web Interface

You can run a simple web interface using **Streamlit**:

```bash
streamlit run note_app/streamlit_app.py
```

Open the provided URL in your browser. The interface offers tabs to record new
notes, query existing ones and edit `notes.txt` or `categories.txt` directly in
the browser.

## Testing the OpenAI API

You can verify your API key and connectivity by running:

```bash
python openai_test.py
```

This script makes a simple request to OpenAI and prints the response.

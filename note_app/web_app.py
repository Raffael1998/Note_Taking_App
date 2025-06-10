from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, render_template, request, redirect, jsonify

from .llm_interface import LLMInterface
from .note_manager import NoteManager
from .categories import load_categories
from .voice_recorder import VoiceRecorder

app = Flask(__name__)
llm = LLMInterface()
notes = NoteManager()
recorder = VoiceRecorder()


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/record', methods=['GET', 'POST'])
def record() -> str | dict:
    if request.method == 'GET':
        return render_template('record.html')
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'message': 'No audio received'}), 400
    language = request.form.get('language', 'en')
    save_path = Path('web_recording.webm')
    audio_file.save(save_path)
    try:
        with open(save_path, 'rb') as f:
            response = recorder.client.audio.transcriptions.create(
                model='whisper-1', file=f, language=language
            )
        text = response.text.strip()
        summary = llm.summarize(text)
        category = llm.infer_category(text, load_categories())
        notes.add_note(summary, category=category)
        message = f"Note added: [{category}] {summary}"
        return jsonify({'message': message})
    except Exception as exc:
        return jsonify({'message': str(exc)}), 500
    finally:
        if save_path.exists():
            os.remove(save_path)


@app.route('/query', methods=['GET', 'POST'])
def query() -> str | dict:
    if request.method == 'GET':
        return render_template('query.html')
    if 'audio' in request.files:
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        save_path = Path('query_recording.webm')
        audio_file.save(save_path)
        try:
            with open(save_path, 'rb') as f:
                response = recorder.client.audio.transcriptions.create(
                    model='whisper-1', file=f, language=language
                )
            query_text = response.text.strip()
        except Exception as exc:
            return jsonify({'result': str(exc)}), 500
        finally:
            if save_path.exists():
                os.remove(save_path)
    else:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'result': 'No query provided'}), 400
        query_text = data['query']

    note_text = notes.read_notes()
    if not note_text.strip():
        return jsonify({'result': 'No notes found'})
    result = llm.query_notes(note_text, query_text)
    return jsonify({'result': result})


def _edit_file(path: Path, content: str | None) -> str:
    if content is not None:
        path.write_text(content, encoding='utf-8')
    return path.read_text(encoding='utf-8')


@app.route('/notes', methods=['GET', 'POST'])
def edit_notes() -> str:
    content = None
    if request.method == 'POST':
        content = request.form.get('content', '')
    text = _edit_file(Path('notes.txt'), content)
    return render_template('notes.html', content=text)


@app.route('/categories', methods=['GET', 'POST'])
def edit_categories() -> str:
    content = None
    if request.method == 'POST':
        content = request.form.get('content', '')
    text = _edit_file(Path('categories.txt'), content)
    return render_template('categories.html', content=text)


if __name__ == '__main__':
    app.run(debug=True)

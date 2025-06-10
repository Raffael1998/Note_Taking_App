from __future__ import annotations

import os
from dataclasses import dataclass

import openai


@dataclass
class LLMInterface:
    """Interface to interact with an LLM, e.g. OpenAI GPT."""

    model: str = "gpt-3.5-turbo"

    def __post_init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable not set")
        openai.api_key = api_key

    def summarize(self, text: str) -> str:
        """Summarize raw text into a short note."""
        prompt = (
            "You are an assistant that writes concise notes."
            " Summarize the following text into a short reminder-style note."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response.choices[0].message["content"].strip()

    def query_notes(self, notes: str, query: str) -> str:
        """Return only lines from notes relevant to the query."""
        prompt = (
            "You are a note assistant. Given the following notes, return only the lines that are relevant to the user's query."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Notes:\n{notes}\nQuery: {query}"},
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response.choices[0].message["content"].strip()

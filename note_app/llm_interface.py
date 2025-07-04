from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI
from dotenv import load_dotenv


@dataclass
class LLMInterface:
    """Interface to interact with an LLM, e.g. OpenAI GPT."""

    model: str = "gpt-4.1-nano"

    def __post_init__(self) -> None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

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
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content.strip()

    def infer_category(self, text: str, categories: list[str] | None = None) -> str:
        """Return the best matching category for the text."""
        if categories:
            category_list = "\n".join(categories)
            prompt = (
                "Select the most appropriate category for the following note "
                "from this list. If nothing fits, answer 'Other'.\n"
                f"Categories:\n{category_list}"
            )
        else:
            prompt = (
                "Provide a concise category for the following note. "
                "Respond with only a short phrase."
            )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content.strip()

    def query_notes(self, notes: str, query: str) -> str:
        """Return full note lines, with timestamps and categories, relevant to the query."""
        prompt = (
            "You are a note assistant. Given the following notes, return only the full original lines (including date and category) that are relevant to the user's query."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Notes:\n{notes}\nQuery: {query}"},
        ]
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content.strip()

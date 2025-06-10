import os

from openai import OpenAI
from dotenv import load_dotenv


def main() -> None:
    """Make a simple call to the OpenAI API and print the response."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(response.choices[0].message.content.strip())


if __name__ == "__main__":
    main()

import os

import openai


def main() -> None:
    """Make a simple call to the OpenAI API and print the response."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(response.choices[0].message["content"].strip())


if __name__ == "__main__":
    main()

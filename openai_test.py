import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    """Make a simple call to the OpenAI API and print the response."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")
    model = os.getenv("NOTE_APP_LLM_MODEL", "gpt-4.1-mini")
    llm = ChatOpenAI(model=model, temperature=0)
    response = llm.invoke("Hello")
    print(response.content.strip())


if __name__ == "__main__":
    main()

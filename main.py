import argparse
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from prompt import system_prompt


def generate_with_retry(client, model, messages, max_retries=50, delay=3):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(system_instruction=system_prompt),
            )
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(delay)
                continue
            raise


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY not found")

    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = generate_with_retry(client, model, messages)

    if (
        response is None
        or response.usage_metadata.prompt_token_count is None
        or response.usage_metadata.candidates_token_count is None
    ):
        raise RuntimeError("Response is None")

    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"User prompt: {args.user_prompt}")
        print(f"Response:\n{response.text}")
    else:
        print(f"Response:\n{response.text}")


print(get_files_info("calculator"))

if __name__ == "__main__":
    main()

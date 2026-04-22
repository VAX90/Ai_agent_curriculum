import argparse
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_functions import available_functions, call_function
from prompt import system_prompt

MODEL_NAME = "gemini-2.5-flash"
MAX_RETRIES = 50
RETRY_DELAY = 3


def get_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found")
    return api_key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args()


def build_messages(user_prompt: str) -> list[types.Content]:
    return [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        )
    ]


def generate_with_retry(
    client: genai.Client,
    model: str,
    messages: list[types.Content],
    max_retries: int = MAX_RETRIES,
    delay: int = RETRY_DELAY,
):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as exc:
            is_503_error = "503" in str(exc)

            if is_503_error and attempt < max_retries - 1:
                time.sleep(delay)
                continue

            raise


def print_usage(response, user_prompt: str, verbose: bool) -> None:
    if not verbose:
        return

    usage = getattr(response, "usage_metadata", None)

    prompt_tokens = getattr(usage, "prompt_token_count", None)
    response_tokens = getattr(usage, "candidates_token_count", None)

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"User prompt: {user_prompt}")


def handle_response(response, user_prompt: str, verbose: bool) -> None:
    if response is None:
        raise RuntimeError("Response is None")

    function_calls = getattr(response, "function_calls", None)

    if function_calls:
        print_usage(response, user_prompt, verbose)

        function_results = []
        for function_call in function_calls:
            result = call_function(function_call, verbose=verbose)

            if not result.parts:
                raise RuntimeError("Empty parts in function call result")
            if result.parts[0].function_response is None:
                raise RuntimeError("Missing function_response")
            if result.parts[0].function_response.response is None:
                raise RuntimeError("Missing response")

            function_results.append(result.parts[0])

            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
        return


def main() -> None:
    args = parse_args()
    api_key = get_api_key()

    client = genai.Client(api_key=api_key)
    messages = build_messages(args.user_prompt)

    response = generate_with_retry(
        client=client,
        model=MODEL_NAME,
        messages=messages,
    )

    handle_response(
        response=response,
        user_prompt=args.user_prompt,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()

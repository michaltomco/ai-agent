import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def get_ai_client(api_key):
    if api_key:
        print("api key loaded")
    else:
        raise RuntimeError("input GEMINI_API_KEY")

    return genai.Client(api_key=api_key)


def get_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser


def generate_content(client, messages):
    return client.models.generate_content(model="gemini-2.5-flash", contents=messages)


def print_response(response, parser_args):
    if not response.usage_metadata:
        raise RuntimeError("Response malformed")

    if parser_args.verbose:
        print(f"User prompt: {parser_args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


def main():
    load_dotenv()

    client = get_ai_client(os.environ.get("GEMINI_API_KEY"))
    parser_args = get_parser().parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=parser_args.user_prompt)])
    ]

    print_response(generate_content(client, messages), parser_args)


if __name__ == "__main__":
    main()

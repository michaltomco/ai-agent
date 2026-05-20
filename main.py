import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def generate_content(client, messages):
    return client.models.generate_content(model="gemini-2.5-flash", contents=messages)


def set_parser(description, arg):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(arg, type=str, help="User prompt")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser


def print_response(response, args):
    if not response.usage_metadata:
        raise RuntimeError("Response malformed")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
        print("api key loaded")
    else:
        raise RuntimeError("API KEY IS NONE")

    client = genai.Client(api_key=api_key)

    args = set_parser("Chatbot", "user_prompt").parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    print_response(generate_content(client, messages), args)


if __name__ == "__main__":
    main()

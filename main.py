import os
from dotenv import load_dotenv
from google import genai
from google.genai.chats import GenerateContentResponse
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
        print("api key loaded")
    else:
        raise RuntimeError("API KEY IS NONE")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    content: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
    )
    if not content.usage_metadata:
        raise RuntimeError("Response malformed")

    print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {content.usage_metadata.candidates_token_count}")

    print(content.text)


if __name__ == "__main__":
    main()

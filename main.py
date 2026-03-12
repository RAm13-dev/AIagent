import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


parser = argparse.ArgumentParser(description="Chatbot")

parser.add_argument("user_prompt", type=str, help="User prompt")

args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
        raise RuntimeError("no api key")

client = genai.Client(api_key=api_key)

def main():
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents= messages)
    print("Response:")
    print(response.text)
    if not response.usage_metadata:
        raise RuntimeError("Failed API request")
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()

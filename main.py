import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

parser = argparse.ArgumentParser(description="Chatbot")

parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("no api key")

client = genai.Client(api_key=api_key)


def main():
    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
        if not response.usage_metadata:
            raise RuntimeError("Failed API request")
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return
        else:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(
                    function_call, verbose=args.verbose
                )
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                    or not function_call_result.parts[0].function_response.response
                ):
                    raise RuntimeError(
                        f"Empty function response for {function_call.name}"
                    )
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
                function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))
    print("Maximum iterations reached without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()

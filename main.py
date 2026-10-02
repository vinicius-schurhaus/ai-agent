import os
import argparse
import json

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function

load_dotenv()


api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured. "
        "Add it to your .env file before running the program."
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)

if response.usage is None:
    raise RuntimeError("The API response did not include token usage information.")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call)

        if not result_message["content"]:
            raise Exception("Tool call returned an empty content")

        if args.verbose:
            print(f"-> {result_message['content']}")
else:
    print(message.content)

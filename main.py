import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("API key wasn't found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages: list[ChatCompletionMessageParam] = [
    {"role": "user", "content": args.user_prompt},
]
response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages
)
verbose = args.verbose
if verbose:
    print(f"User prompt: {args.user_prompt}")
    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("response.usage is None")
print(f"Response: {response.choices[0].message.content}")

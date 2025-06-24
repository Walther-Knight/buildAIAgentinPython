import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 main.py <"prompt"> <optional switch>. Retry with proper syntax.')
        sys.exit(1)

    prompt_value = sys.argv[1]
    if len(sys.argv) > 2:
        switch_value = sys.argv[2]
    else:
        switch_value = 0

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt_value)]),
]

    response = client.models.generate_content(
        model= "gemini-2.0-flash-001", contents=messages
        )
    if switch_value == "--verbose":
        print(f"User prompt: {prompt_value}\nResponse: {response.text}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(f"Response: {response.text}")
    


if __name__ == "__main__":
    main()
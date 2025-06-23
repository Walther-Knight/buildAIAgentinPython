import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 main.py <"prompt">. Retry with proper syntax.')
        sys.exit(1)

    prompt_value = sys.argv[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model= "gemini-2.0-flash-001", contents= prompt_value
        )
    print(f"Response: {response.text}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
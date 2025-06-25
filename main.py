import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 main.py <"prompt"> <optional switch>. Retry with proper syntax.')
        sys.exit(1)

    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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

    schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
   # schema_get_file_content = types.FunctionDeclaration(
    #name="get_file_content",
    #description="Gets the contents of a file, constrained to the working directory.",
    #parameters=types.Schema(
     #   type=types.Type.OBJECT,
      #  properties={
       #     "directory": types.Schema(
        #        type=types.Type.STRING,
         #       description="The file to get contents from, relative to the working directory. If not provided returns an error.",
          #  ),
        #},
    #),
#)

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
    response = client.models.generate_content(
        model= "gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
        )
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        if switch_value == "--verbose":
            print(f"User prompt: {prompt_value}\nResponse: {response.text}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print(f"Response: {response.text}")
    


if __name__ == "__main__":
    main()
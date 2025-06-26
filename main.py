import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

#Define global
working_directory = "./calculator"
legal_functions = {"get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
}  

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 main.py <"prompt"> <optional switch>. Retry with proper syntax.')
        sys.exit(1)

    system_prompt = system_prompt = """You are a helpful coding assistant with access to file system tools. 

You MUST use the available tools to explore and understand the codebase before answering questions. When a user asks about code functionality:

1. FIRST use get_files_info with directory="." to see what files are available
2. THEN use get_file_content to examine relevant files
3. Use run_python_file if you need to test functionality
4. Use write_file if you need to create or modify files

Always start by exploring the file system. Don't ask the user for file paths - discover them yourself using the tools.

The working_directory parameter is hard-coded for safety.

Available tools:
- get_files_info: Lists files in a directory (use "." for current directory)
- get_file_content: Gets contents of a file
- run_python_file: Runs a Python file
- write_file: Writes content to a file

Be proactive and use these tools to investigate the codebase!"""

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
    max_iterations = 20
    iteration = 0

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
        required=["directory"]
    ),
)
    schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get contents from, relative to the working directory. If not provided returns an error.",
            ),
        },
        required=["file_path"]
    ),
)
    
    schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file with arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to execute, relative to the working directory. If not provided returns an error.",
            ),
        },
        required=["file_path"]
    ),
)
    
    schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a specified file with specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to write, relative to the working directory. If not provided returns an error. If file does not exist, file is created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided returns an error.",
            ),
        },
        required=["file_path", "content"]
    ),
)

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
    while iteration < max_iterations:
        response = client.models.generate_content(
            model= "gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
                ),
            )
        for candidate in response.candidates:
            messages.append(candidate.content)
        function_called = False
        if response.function_calls:
            function_called = True
            for function_call in response.function_calls:
                if switch_value == "--verbose":
                    function_call_result = call_function(function_call, True)
                else:
                    function_call_result = call_function(function_call)

                if not function_call_result.parts[0].function_response.response:
                    raise "Fatal Error: function_call did not return a response"

                messages.append(function_call_result)
        if not function_called:
            print("Final Response:")
            print(response.text)
            break
        iteration += 1
            
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args["working_directory"] = working_directory
    if function_name not in legal_functions:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
    function_result = legal_functions[function_name](**function_args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)


if __name__ == "__main__":
    main()
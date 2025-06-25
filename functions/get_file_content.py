import os

def get_file_content(working_directory, file_path):
    rel_path = os.path.abspath(working_directory)
    temp_path = os.path.join(working_directory, file_path)
    final_path = os.path.abspath(temp_path)
    if not final_path.startswith(rel_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    is_file = os.path.isfile(final_path)
    if not is_file:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    with open(final_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    if len(file_content_string) == 10000:
        return file_content_string + f"...File {file_path} truncated at 10000 characters"
    return file_content_string

import os

def write_file(working_directory, file_path, content):
    rel_path = os.path.abspath(working_directory)
    temp_path = os.path.join(working_directory, file_path)
    final_path = os.path.abspath(temp_path)
    dir_path = os.path.dirname(final_path)
    if not final_path.startswith(rel_path):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    try:      
        path_exists =  os.path.exists(dir_path)
        if not path_exists:
            os.makedirs(dir_path)
        with open(final_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


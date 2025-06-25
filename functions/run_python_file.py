import os
import subprocess

def run_python_file(working_directory, file_path):
    rel_path = os.path.abspath(working_directory)
    temp_path = os.path.join(working_directory, file_path)
    final_path = os.path.abspath(temp_path)
    if not final_path.startswith(rel_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    file_exists = os.path.exists(final_path)
    if not file_exists:
        return f'Error: File "{file_path}" not found.'
    if not final_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python3", final_path], timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    if not result.stderr and not result.stdout:
        return "No output produced."
    else: 
        output = f"STDOUT: {result.stdout.decode('utf-8')}\nSTDERR: {result.stderr.decode('utf-8')}"
    if result.returncode != 0:
        output += f"\nProcess exited with code {result.returncode}"

    return output
    
    

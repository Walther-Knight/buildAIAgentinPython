import os

def get_files_info(working_directory, directory=None):
    rel_path = os.path.abspath(working_directory)
    temp_path = os.path.join(working_directory, directory)
    dir_path = os.path.abspath(temp_path)
    if not dir_path.startswith(rel_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    is_dir = os.path.isdir(dir_path)
    if not is_dir:
        return f'Error: "{directory}" is not a directory'
    
    dir_list = [dir_path]
    output = ""
    while dir_list:
        current_dir = dir_list.pop()
        file_list = os.listdir(current_dir)
        for file in file_list:
            try:
                file_path = os.path.join(current_dir, file)
                f_size = os.path.getsize(file_path)
                f_dir = os.path.isdir(file_path)
            except Exception as e:
                return f"Error: An OS error occurred: {e}"
            output += f"- {file}: file_size={f_size} bytes, is_dir={f_dir}\n"
            if f_dir:
                dir_list.append(file_path)
    return output


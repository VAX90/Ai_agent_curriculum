import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    try:
        if os.path.commonpath([abs_working_dir, abs_target_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.commonpath([abs_working_dir, abs_target_path]):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.commonpath([abs_working_dir, abs_target_path]) == abs_working_dir:
            os.makedirs(os.path.join(working_directory, file_path))
        with open(os.path.join(working_directory, file_path), "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
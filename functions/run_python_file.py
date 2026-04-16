import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs, file_path))
    if not target_file.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", target_file]
    if args:
        command.extend(args)
    result = subprocess.run(
        command, cwd=working_directory, capture_output=True, text=True, timeout=30
    )
    output = ""
    try:
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced\n"
        else:
            if result.stdout:
                output += f"STDOUT: {result.stdout}"
            if result.stderr:
                output += f"STDERR: {result.stderr}"
        return output
    except Exception as e:
        return f"Executin Python file: {e}"

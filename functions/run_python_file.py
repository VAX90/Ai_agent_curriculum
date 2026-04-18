import os
import subprocess
from google.genai import types



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its stdout/stderr output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file to be run in the provided working directory, you shall only pass files that are within the provided working directory itself or in nested subdirectories within thath"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                   type=types.Type.STRING,
                  description="One argument string, equivalent to a single entry in sys.argv[1:]" 
                ),
                description="list of argument/s to provide for the runtime"
            )
        },
        required=["file_path"],
    ),
)

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
    try:
        result = subprocess.run(
            command, cwd=os.path.abspath(working_directory), capture_output=True, text=True, timeout=30
        )
        output = ""
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
        return f"Error: executing Python file: {e}"

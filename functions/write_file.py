from pathlib import Path
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="modification to write in file inside the working directory you need to stay within",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file needs to be worked on in the provided working directory, you shall only pass files that are within the provided working directory itself or in nested subdirectories within thath"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="modification to write in file inside the working directory you need to stay within."
            )
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        base = Path(working_directory).resolve()
        target = (base / file_path).resolve()

        if base not in target.parents and target != base:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {str(e)}"

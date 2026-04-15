from pathlib import Path


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

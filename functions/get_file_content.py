import os
from config import MAX_CHARS
from google.genai import types



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read and get content of specified file inside the working directory you need to stay within, file will get truncated at 10000 bytes if longer",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file needs to be worked on in the provided working directory, you shall only pass files that are within the provided working directory itself or in nested subdirectories within thath"
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # Costruisce il path assoluto sicuro
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # Sicurezza: evita path traversal (../ ecc)
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Controllo esistenza file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Lettura file
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Troncamento
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"


def main():
    # esempio base, perché prima non passavi nulla (geniale)
    working_directory = "."
    file_path = "example.txt"

    result = get_file_content(working_directory, file_path)
    print(result)


if __name__ == "__main__":
    main()
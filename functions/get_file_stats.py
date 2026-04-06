import os

from google.genai import types


def get_file_stats(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_filepath]) != working_dir_abs:
            return f'Error: Cannot inspect "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_filepath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        size = os.path.getsize(target_filepath)
        with open(target_filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if content == "":
            lines = 0
        elif content.endswith("\n"):
            lines = content.count("\n")
        else:
            lines = content.count("\n") + 1

        words = len(content.split())
        characters = len(content)

        return (
            f'File statistics for "{file_path}":\n'
            f'- size={size} bytes\n'
            f'- lines={lines}\n'
            f'- words={words}\n'
            f'- characters={characters}'
        )
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_file_stats = types.FunctionDeclaration(
    name="get_file_stats",
    description="Returns line, word, character, and byte counts for a file within the sandbox",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

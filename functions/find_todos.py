import os

from google.genai import types


def find_todos(working_directory, directory=".", markers=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot search "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        markers = markers or ["TODO", "FIXME"]
        matches = []
        for root, _, filenames in os.walk(target_dir):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for lineno, line in enumerate(f, start=1):
                            for marker in markers:
                                if marker in line:
                                    rel_path = os.path.relpath(filepath, working_dir_abs)
                                    matches.append(f"{rel_path}:{lineno}: {line.strip()}")
                                    break
                except Exception:
                    continue

        if not matches:
            return f"No TODO/FIXME markers found under '{directory}'"

        return "\n".join(matches)
    except Exception as e:
        return f"Error: {str(e)}"


schema_find_todos = types.FunctionDeclaration(
    name="find_todos",
    description="Finds TODO and FIXME markers in files under the sandbox.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path relative to the working directory to search",
            ),
        },
    ),
)

import os
import re

from google.genai import types


def summarize_code(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_filepath]) != working_dir_abs:
            return f'Error: Cannot summarize "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_filepath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        lines = content.splitlines()
        imports = []
        functions = []
        classes = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                imports.append(stripped)
            elif re.match(r"^def \w+\(", stripped):
                functions.append(stripped)
            elif re.match(r"^class \w+\(", stripped) or re.match(r"^class \w+:", stripped):
                classes.append(stripped)

        summary = [
            f"File: {file_path}",
            f"- lines={len(lines)}",
            f"- imports={len(imports)}",
            f"- functions={len(functions)}",
            f"- classes={len(classes)}",
            "- top imports:",
        ]
        summary.extend([f"  - {line}" for line in imports[:10]])
        summary.append("- top functions/classes:")
        for item in (functions + classes)[:10]:
            summary.append(f"  - {item}")

        return "\n".join(summary)
    except Exception as e:
        return f"Error: {str(e)}"


schema_summarize_code = types.FunctionDeclaration(
    name="summarize_code",
    description="Summarizes the structure of a Python source file within the sandbox.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a Python file relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

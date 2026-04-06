import json
import os
import time

from google.genai import types


def _resolve_path(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target_filepath]) != working_dir_abs:
        raise ValueError(
            f'Cannot access "{file_path}" as it is outside the permitted working directory'
        )
    return target_filepath


def load_context(working_directory, file_path=".agent_context.json"):
    try:
        target_filepath = _resolve_path(working_directory, file_path)
        if not os.path.exists(target_filepath):
            return "[]"
        with open(target_filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"


def append_context(working_directory, content, file_path=".agent_context.json"):
    try:
        target_filepath = _resolve_path(working_directory, file_path)
        directory = os.path.dirname(target_filepath)
        os.makedirs(directory, exist_ok=True)

        if os.path.exists(target_filepath):
            with open(target_filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        if not isinstance(data, list):
            data = [data]

        entry = {
            "timestamp": int(time.time()),
            "content": content,
        }
        data.append(entry)

        with open(target_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return f"Appended context entry to {file_path} ({len(data)} entries total)"
    except Exception as e:
        return f"Error: {str(e)}"


schema_load_context = types.FunctionDeclaration(
    name="load_context",
    description="Loads the local context file from the sandboxed working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the local context file",
            ),
        },
    ),
)

schema_append_context = types.FunctionDeclaration(
    name="append_context",
    description="Appends a new context entry to the local context file in the sandbox.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text to append to the context file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the local context file",
            ),
        },
        required=["content"],
    ),
)

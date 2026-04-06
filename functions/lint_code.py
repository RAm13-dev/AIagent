import os
import py_compile

from google.genai import types


def lint_code(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot lint "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        py_files = []
        for root, _, filenames in os.walk(target_dir):
            for filename in filenames:
                if filename.endswith(".py"):
                    py_files.append(os.path.join(root, filename))

        if not py_files:
            return "No Python files found to lint"

        errors = []
        for path in py_files:
            try:
                py_compile.compile(path, doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(str(exc))

        if errors:
            return "Errors:\n" + "\n\n".join(errors)

        return f"Lint passed for {len(py_files)} Python files"
    except Exception as e:
        return f"Error: {str(e)}"


schema_lint_code = types.FunctionDeclaration(
    name="lint_code",
    description="Performs syntax-only linting of Python files in a directory within the sandbox.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path relative to the working directory to lint",
            ),
        },
    ),
)

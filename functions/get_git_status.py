import os
import subprocess

from google.genai import types


def get_git_status(working_directory):
    try:
        command = ["git", "status", "--short", "--branch"]
        result = subprocess.run(
            command,
            cwd=os.path.abspath(working_directory),
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode != 0:
            return f"Error: git status failed: {result.stderr.strip()}"

        output = result.stdout.strip()
        return output or "Clean working tree"
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_git_status = types.FunctionDeclaration(
    name="get_git_status",
    description="Returns the current git branch and working tree status from the repository.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)

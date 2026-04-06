import os
import subprocess
import sys

from google.genai import types


def run_tests(working_directory, test_directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, test_directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot run tests in "{test_directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{test_directory}" is not a directory'

        commands = [
            [sys.executable, "-m", "unittest", "discover", "-s", target_dir, "-p", "test_*.py"],
        ]

        tests_py = os.path.join(target_dir, "tests.py")
        if os.path.isfile(tests_py):
            commands.append([sys.executable, tests_py])

        output_parts = []
        for command in commands:
            result = subprocess.run(
                command,
                cwd=target_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            output_parts.append("Command: " + " ".join(command))
            if result.stdout:
                output_parts.append("STDOUT:\n" + result.stdout.strip())
            if result.stderr:
                output_parts.append("STDERR:\n" + result.stderr.strip())

            if result.returncode != 0:
                combined_output = (result.stdout or "") + (result.stderr or "")
                if command[1:] == ["-m", "unittest", "discover", "-s", target_dir, "-p", "test_*.py"]:
                    if "NO TESTS RAN" in combined_output:
                        continue
                output_parts.append(f"Command exited with code {result.returncode}")
                return "\n\n".join(output_parts)

        return "\n\n".join(output_parts) or "No tests were executed"
    except Exception as e:
        return f"Error: {str(e)}"


schema_run_tests = types.FunctionDeclaration(
    name="run_tests",
    description="Runs unit tests in the specified directory within the sandbox.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "test_directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path relative to the working directory where tests should be run",
            ),
        },
    ),
)

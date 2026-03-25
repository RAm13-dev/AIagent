import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
    
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
        valid_target_dir = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
    
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isfile(absolute_file_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if absolute_file_path.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        return "\n".join(output)
    except Exception as e:
        raise f"Error: executing Python file: {e}"
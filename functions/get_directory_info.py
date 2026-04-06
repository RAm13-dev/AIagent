import os

from google.genai import types


def get_directory_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot inspect "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        file_count = 0
        directory_count = 0
        total_size = 0
        file_sizes = []

        for root, dirs, files in os.walk(target_dir):
            directory_count += len(dirs)
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                except OSError:
                    continue
                file_count += 1
                total_size += size
                rel_path = os.path.relpath(filepath, working_dir_abs)
                file_sizes.append((size, rel_path))

        file_sizes.sort(reverse=True)
        top_files = file_sizes[:5]
        top_file_lines = [f"- {path}: {size} bytes" for size, path in top_files]

        return (
            f'Directory information for "{directory}":\n'
            f'- total_files={file_count}\n'
            f'- total_directories={directory_count}\n'
            f'- total_size={total_size} bytes\n'
            f'- largest_files:\n{chr(10).join(top_file_lines)}'
        )
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_directory_info = types.FunctionDeclaration(
    name="get_directory_info",
    description="Returns summary information for a directory within the sandbox",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path relative to the working directory",
            ),
        },
    ),
)

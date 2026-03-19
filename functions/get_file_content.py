import os

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        valid_target_filepath = os.path.commonpath([working_dir_abs, target_filepath]) == working_dir_abs
        
        if valid_target_filepath == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_filepath) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with open(target_filepath, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
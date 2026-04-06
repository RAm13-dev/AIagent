import os

from google.genai import types


def search_in_files(working_directory, query, directory=".", case_insensitive=False):
    try:
        if not query:
            return "Error: query text must not be empty"

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot search "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        normalized_query = query.lower() if case_insensitive else query
        matches = []
        max_matches = 100

        for root, _, filenames in os.walk(target_dir):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, working_dir_abs)

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line_number, line in enumerate(f, start=1):
                            candidate = line.lower() if case_insensitive else line
                            if normalized_query in candidate:
                                matches.append(
                                    f"{rel_path}: line {line_number}: {line.strip()}"
                                )
                                if len(matches) >= max_matches:
                                    return (
                                        "\n".join(matches)
                                        + "\n[Search truncated after 100 matches]"
                                    )
                except Exception:
                    continue

        if not matches:
            return f'No occurrences of "{query}" found under "{directory}"'

        return "\n".join(matches)
    except Exception as e:
        return f"Error: {str(e)}"


schema_search_in_files = types.FunctionDeclaration(
    name="search_in_files",
    description="Searches files under a directory for a text query and returns matching file paths and lines",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="Text to search for",
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path relative to the working directory",
            ),
            "case_insensitive": types.Schema(
                type=types.Type.BOOLEAN,
                description="Whether to perform a case-insensitive search",
            ),
        },
        required=["query"],
    ),
)

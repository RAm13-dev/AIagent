from google.genai import types

from functions.get_directory_info import get_directory_info, schema_get_directory_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_file_stats import get_file_stats, schema_get_file_stats
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_url_content import get_url_content, schema_get_url_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.search_in_files import search_in_files, schema_search_in_files
from functions.search_web import search_web, schema_search_web
from functions.summarize_code import summarize_code, schema_summarize_code
from functions.write_file import schema_write_file, write_file
from functions.deep_research import deep_research, schema_deep_research
from functions.read_pdf import read_pdf, schema_read_pdf
from functions.get_git_status import get_git_status, schema_get_git_status
from functions.find_todos import find_todos, schema_find_todos
from functions.lint_code import lint_code, schema_lint_code
from functions.run_tests import run_tests, schema_run_tests
from functions.context_store import (
    append_context,
    load_context,
    schema_append_context,
    schema_load_context,
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_get_file_stats,
        schema_get_directory_info,
        schema_search_in_files,
        schema_search_web,
        schema_deep_research,
        schema_get_url_content,
        schema_summarize_code,
        schema_find_todos,
        schema_get_git_status,
        schema_lint_code,
        schema_run_tests,
        schema_read_pdf,
        schema_load_context,
        schema_append_context,
        schema_run_python_file,
        schema_write_file,
    ],
)


def call_function(function_call, verbose=False):

    if verbose == True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "get_file_stats": get_file_stats,
        "get_directory_info": get_directory_info,
        "search_in_files": search_in_files,
        "search_web": search_web,
        "deep_research": deep_research,
        "read_pdf": read_pdf,
        "get_url_content": get_url_content,
        "summarize_code": summarize_code,
        "find_todos": find_todos,
        "get_git_status": get_git_status,
        "lint_code": lint_code,
        "run_tests": run_tests,
        "load_context": load_context,
        "append_context": append_context,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./projects"
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

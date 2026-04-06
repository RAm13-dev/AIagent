# AI Agent

A minimal Python-based AI agent project that integrates with Google Gemini and exposes a set of sandboxed tool functions for file inspection, code execution, and file writing.

The project also includes a small example `projects` subpackage to demonstrate how the agent can inspect and run local Python code safely within a restricted working directory.

## What this project does

- Uses `google-genai` to communicate with the Gemini API
- Defines tool functions for:
  - listing files and directories
  - reading file contents
  - executing Python files
  - writing files
- Wraps these tools in a function-calling interface for the AI model
- Restricts tool access to the `projects` working directory for safety
- Includes a simple example project under `projects/`

## Repository structure

- `main.py` — entrypoint for the AI agent
- `prompts.py` — system prompt used by the Gemini model
- `call_function.py` — maps function calls returned by Gemini to local Python functions
- `functions/` — tool implementations used by the AI agent
- `projects/` — sandboxed example workspace used by the tool functions
  - `main.py` — command-line project runner
  - `pkg/calculator.py` — expression evaluator
  - `pkg/render.py` — JSON formatting helper
- `tests/` — verification scripts for each tool
- `pyproject.toml` — dependency and metadata configuration
- `.env` — environment file for API keys (not committed)

## Requirements

- Python 3.13 or newer
- `google-genai`
- `python-dotenv`

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

> If `requirements.txt` is not present, install directly from `pyproject.toml`:
>
> ```bash
> python -m pip install google-genai==1.12.1 python-dotenv==1.1.0
> ```

3. Create a `.env` file in the project root with your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

## Running the AI agent

To start the agent with a prompt:

```bash
python main.py "Inspect the projects module and tell me what it does."
```

Use `--verbose` to print prompt/response token counts and function-call logs:

```bash
python main.py "Read the projects README file." --verbose
```

Use `--max-iterations` to allow more tool/response passes for deeper reasoning:

```bash
python main.py "Research the latest AI model updates." --max-iterations 30
```

## Using the projects example

The `projects` folder contains a small example project and PDF reading workspace.

Run it directly with:

```bash
python projects/main.py "3 + 5"
```

Example output:

```json
{
  "expression": "3 + 5",
  "result": 8
}
```

## Tool functions

The AI agent exposes these functions through Gemini function calling:

- `get_files_info` — list files and directories under the sandbox
- `get_file_content` — read contents of a file under the sandbox
- `get_file_stats` — show line, word, character, and byte counts for a file
- `get_directory_info` — summarize total files, directories, size, and largest files
- `search_in_files` — search text across files in a directory
- `search_web` — search the internet for real-world information and return result titles, URLs, and snippets
- `deep_research` — gather deeper web research results and optionally fetch page content from top results
- `get_url_content` — fetch text content from a URL on the web
- `read_pdf` — read text from a PDF file inside the sandbox
- `summarize_code` — summarize the structure of a Python source file
- `find_todos` — find TODO/FIXME markers in code and documentation
- `get_git_status` — inspect git branch and working tree status
- `lint_code` — perform syntax-only linting of Python files
- `run_tests` — run unit tests in the sandboxed directory
- `load_context` — load the local agent context file
- `append_context` — append a new entry to the local agent context file
- `run_python_file` — execute a Python file inside the sandbox
- `write_file` — write or overwrite files inside the sandbox

The sandbox directory is currently fixed to `./projects` in `call_function.py`. Internet tools are not restricted by this sandbox and can fetch or search real-world online content when available.

A local context file named `.agent_context.json` can also be used to store agent context entries in the sandbox. This file is stored locally and is ignored by Git.

## Testing

Run the provided test scripts to verify the tool implementations:

```bash
python tests/test_get_file_content.py
python tests/test_get_files_info.py
python tests/test_get_file_stats.py
python tests/test_get_directory_info.py
python tests/test_search_in_files.py
python tests/test_search_web.py
python tests/test_deep_research.py
python tests/test_read_pdf.py
python tests/test_get_url_content.py
python tests/test_summarize_code.py
python tests/test_find_todos.py
python tests/test_get_git_status.py
python tests/test_lint_code.py
python tests/test_run_tests.py
python tests/test_context_store.py
python tests/test_run_python_file.py
python tests/test_write_file.py
```

## Notes

- `main.py` expects a valid `GEMINI_API_KEY` in `.env`
- The agent is intentionally limited to the `projects` directory for security
- The project is a good starting point for building a more capable local AI tool runner

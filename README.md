# AI Agent

A minimal Python-based AI agent project that integrates with Google Gemini and exposes a set of sandboxed tool functions for file inspection, code execution, and file writing.

The project also includes a small example `calculator` subpackage to demonstrate how the agent can inspect and run local Python code safely within a restricted working directory.

## What this project does

- Uses `google-genai` to communicate with the Gemini API
- Defines tool functions for:
  - listing files and directories
  - reading file contents
  - executing Python files
  - writing files
- Wraps these tools in a function-calling interface for the AI model
- Restricts tool access to the `calculator` working directory for safety
- Includes a simple calculator app under `calculator/`

## Repository structure

- `main.py` — entrypoint for the AI agent
- `prompts.py` — system prompt used by the Gemini model
- `call_function.py` — maps function calls returned by Gemini to local Python functions
- `functions/` — tool implementations used by the AI agent
- `calculator/` — sandboxed example workspace used by the tool functions
  - `main.py` — command-line calculator runner
  - `pkg/calculator.py` — expression evaluator
  - `pkg/render.py` — JSON formatting helper
- `test_*.py` — simple scripts to verify each tool individually
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
python main.py "Inspect the calculator module and tell me what it does."
```

Use `--verbose` to print prompt/response token counts and function-call logs:

```bash
python main.py "Read the calculator README file." --verbose
```

## Using the calculator example

The `calculator` folder contains a small expression evaluator.

Run it directly with:

```bash
python calculator/main.py "3 + 5"
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
- `run_python_file` — execute a Python file inside the sandbox
- `write_file` — write or overwrite files inside the sandbox

The sandbox directory is currently fixed to `./calculator` in `call_function.py`.

## Testing

Run the provided test scripts to verify the tool implementations:

```bash
python test_get_file_content.py
python test_get_files_info.py
python test_run_python_file.py
python test_write_file.py
```

## Notes

- `main.py` expects a valid `GEMINI_API_KEY` in `.env`
- The agent is intentionally limited to the `calculator` directory for security
- The project is a good starting point for building a more capable local AI tool runner

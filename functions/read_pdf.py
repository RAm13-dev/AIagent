import os

from google.genai import types
from PyPDF2 import PdfReader


def read_pdf(
    working_directory,
    path,
    page=None,
    start_page=None,
    end_page=None,
    max_chars=10000,
):
    try:
        if not path:
            return "Error: path must not be empty"

        path = os.path.normpath(path)
        if os.path.isabs(path):
            return "Error: path must be relative to the working directory"

        abs_working_dir = os.path.abspath(working_directory)
        pdf_path = os.path.abspath(os.path.join(abs_working_dir, path))
        if os.path.commonpath([abs_working_dir, pdf_path]) != abs_working_dir:
            return f'Error: Cannot access "{path}" outside the permitted working directory'

        if not os.path.isfile(pdf_path):
            return f'Error: File not found: "{path}"'

        if not pdf_path.lower().endswith(".pdf"):
            return f'Error: File is not a PDF: "{path}"'

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        if page is not None:
            start_page = page
            end_page = page

        if start_page is None:
            start_page = 1
        if end_page is None:
            end_page = num_pages

        if start_page < 1 or end_page < 1 or start_page > num_pages or end_page > num_pages:
            return f"Error: page range must be between 1 and {num_pages}"
        if start_page > end_page:
            return "Error: start_page cannot be greater than end_page"

        pages_text = []
        collected = []
        total_chars = 0
        for page_number in range(start_page, end_page + 1):
            page_obj = reader.pages[page_number - 1]
            text = page_obj.extract_text() or ""
            pages_text.append({
                "page": page_number,
                "text": text,
            })
            if total_chars < max_chars:
                available = max_chars - total_chars
                chunk = text[:available]
                collected.append(chunk)
                total_chars += len(chunk)
            if total_chars >= max_chars:
                break

        truncated_text = "\n\n".join(collected)
        if total_chars >= max_chars:
            truncated_text += f"\n...[truncated at {max_chars} characters]"

        return {
            "path": path,
            "num_pages": num_pages,
            "pages": pages_text,
            "text": truncated_text,
        }
    except Exception as e:
        return f"Error: {str(e)}"


schema_read_pdf = types.FunctionDeclaration(
    name="read_pdf",
    description="Reads text from a PDF file in the working directory and returns the extracted page content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "path": types.Schema(
                type=types.Type.STRING,
                description="Path to the PDF file relative to the working directory.",
            ),
            "page": types.Schema(
                type=types.Type.INTEGER,
                description="Single page number to read (1-indexed).",
            ),
            "start_page": types.Schema(
                type=types.Type.INTEGER,
                description="First page number to read (1-indexed).",
            ),
            "end_page": types.Schema(
                type=types.Type.INTEGER,
                description="Last page number to read (1-indexed).",
            ),
            "max_chars": types.Schema(
                type=types.Type.INTEGER,
                description="Maximum number of characters to return from the PDF text.",
            ),
        },
        required=["path"],
    ),
)

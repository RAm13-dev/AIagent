import urllib.request
from urllib.parse import urlparse

from google.genai import types


def get_url_content(working_directory, url, max_chars=10000):
    try:
        if not url:
            return "Error: url must not be empty"

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return "Error: url must start with http:// or https://"

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; AI-Agent/1.0; +https://example.com)"
            },
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read(max_chars + 1)
            content = raw.decode("utf-8", errors="ignore")

        if len(content) > max_chars:
            return content[:max_chars] + f"\n...[content truncated at {max_chars} characters]"
        return content
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_url_content = types.FunctionDeclaration(
    name="get_url_content",
    description="Fetches the text content of a URL from the web, limited to a safe character count.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "url": types.Schema(
                type=types.Type.STRING,
                description="The URL to fetch content from",
            ),
            "max_chars": types.Schema(
                type=types.Type.INTEGER,
                description="Maximum number of characters to return",
            ),
        },
        required=["url"],
    ),
)

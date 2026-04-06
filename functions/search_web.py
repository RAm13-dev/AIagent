import re
import urllib.parse
import urllib.request

from google.genai import types


def search_web(working_directory, query, max_results=5):
    try:
        if not query:
            return "Error: query must not be empty"

        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; AI-Agent/1.0; +https://example.com)"
            },
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            html = response.read().decode("utf-8", errors="ignore")

        results = []
        for match in re.finditer(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            html,
            re.IGNORECASE | re.DOTALL,
        ):
            if len(results) >= max_results:
                break
            title = re.sub(r"<.*?>", "", match.group(2)).strip()
            link = match.group(1).strip()
            snippet_match = re.search(
                r'<a[^>]+href="%s"[^>]*>.*?</a>\s*<div[^>]+class="result__snippet"[^>]*>(.*?)</div>'
                % re.escape(link),
                html,
                re.IGNORECASE | re.DOTALL,
            )
            snippet = (
                re.sub(r"<.*?>", "", snippet_match.group(1)).strip()
                if snippet_match
                else ""
            )
            results.append(f"{title}\n{link}\n{snippet}")

        if not results:
            return f"No results found for '{query}'"

        return "\n\n".join(results)
    except Exception as e:
        return f"Error: {str(e)}"


schema_search_web = types.FunctionDeclaration(
    name="search_web",
    description="Searches the internet for a query and returns a small set of result titles, URLs, and snippets.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="Search query text",
            ),
            "max_results": types.Schema(
                type=types.Type.INTEGER,
                description="Maximum number of search results to return",
            ),
        },
        required=["query"],
    ),
)

import html
import re

from google.genai import types

from functions.get_url_content import get_url_content
from functions.search_web import search_web


def deep_research(
    working_directory,
    query,
    max_results=5,
    fetch_pages=False,
    max_page_chars=2000,
):
    try:
        if not query:
            return "Error: query must not be empty"

        raw_results = search_web(working_directory, query, max_results)
        if isinstance(raw_results, str) and (
            raw_results.startswith("Error:") or raw_results.startswith("No results")
        ):
            return raw_results

        results = []
        for block in raw_results.split("\n\n"):
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if len(lines) < 2:
                continue
            title = html.unescape(lines[0])
            url = html.unescape(lines[1])
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("/"):
                url = "https://html.duckduckgo.com" + url
            snippet = html.unescape("\n".join(lines[2:]).strip() if len(lines) > 2 else "")
            page_content = None
            if fetch_pages:
                page_content = get_url_content(working_directory, url, max_chars=max_page_chars)
            entry = {
                "title": title,
                "url": url,
                "snippet": snippet,
            }
            if fetch_pages:
                entry["page_content"] = page_content
            results.append(entry)

        if not results:
            return f"No extractable web results found for '{query}'"

        return {
            "query": query,
            "results": results,
        }
    except Exception as e:
        return f"Error: {str(e)}"


schema_deep_research = types.FunctionDeclaration(
    name="deep_research",
    description="Performs a deeper web research query and optionally fetches content from top results.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="Search query text.",
            ),
            "max_results": types.Schema(
                type=types.Type.INTEGER,
                description="Maximum number of search results to return.",
            ),
            "fetch_pages": types.Schema(
                type=types.Type.BOOLEAN,
                description="Whether to fetch page content from each search result.",
            ),
            "max_page_chars": types.Schema(
                type=types.Type.INTEGER,
                description="Maximum number of characters to fetch from each page when fetching page content.",
            ),
        },
        required=["query"],
    ),
)

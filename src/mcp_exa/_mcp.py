"""MCP server implementation for Exa search API."""

import os
from typing import Any

import fastmcp
import httpx

mcp = fastmcp.FastMCP("mcp-exa")

EXA_API_BASE = "https://api.exa.ai"


def get_api_key() -> str:
    """Get Exa API key from environment variable."""
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise ValueError(
            "EXA_API_KEY environment variable is not set. "
            "Please set it with your Exa API key. "
            "Get your API key at https://dashboard.exa.ai/api-keys"
        )
    return api_key


async def _make_request(
    endpoint: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Make request to Exa API."""
    api_key = get_api_key()
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{EXA_API_BASE}/{endpoint}",
            json=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]


@mcp.tool()
async def web_search_exa(
    query: str,
    num_results: int = 10,
    text_max_characters: int = 0,
    summary_query: str = "",
) -> dict[str, Any]:
    """Search the web for any topic and get clean, ready-to-use content.

    Args:
        query: The search query string.
        num_results: Number of results to return (default: 10).
        text_max_characters: Maximum characters per result (0 for unlimited).
        summary_query: Query to generate AI summary of results.

    Returns:
        Dictionary containing search results with title, url, content.

    Example:
        >>> web_search_exa("Python asyncio best practices")
        {"results": [...]}
    """
    if not query or not query.strip():
        return {"results": [], "message": "Query cannot be empty"}

    payload: dict[str, Any] = {
        "query": query,
        "numResults": num_results,
    }

    if text_max_characters > 0:
        payload["textMaxCharacters"] = text_max_characters

    if summary_query:
        payload["summaryQuery"] = summary_query
        payload["enableSummary"] = True

    return await _make_request("search", payload)


@mcp.tool()
async def get_code_context_exa(
    query: str,
    tokens_num: int = 5000,
) -> dict[str, Any]:
    """Find code examples, documentation, and programming solutions from GitHub, Stack Overflow, and docs.

    Args:
        query: The code search query string.
        tokens_num: Context length in tokens (default: 5000, typical range: 1000-50000).

    Returns:
        Dictionary containing code examples with source URLs.

    Example:
        >>> get_code_context_exa("Python FastMCP server example")
        {"results": [...]}
    """
    if not query or not query.strip():
        return {"results": [], "message": "Query cannot be empty"}

    payload: dict[str, Any] = {
        "query": query,
        "tokensNum": tokens_num,
    }

    return await _make_request("search", payload)


@mcp.tool()
async def crawling_exa(
    url: str,
    query: str = "",
    text_max_characters: int = 0,
) -> dict[str, Any]:
    """Get the full content of a specific webpage from a known URL.

    Args:
        url: The URL to crawl.
        query: Query to extract relevant content.
        text_max_characters: Maximum characters to extract (0 for unlimited).

    Returns:
        Dictionary containing extracted content from the URL.

    Example:
        >>> crawling_exa("https://github.com/exa-labs/exa-mcp-server")
        {"results": [...]}
    """
    if not url or not url.strip():
        return {"results": [], "message": "URL cannot be empty"}

    payload: dict[str, Any] = {
        "url": url,
    }

    if query:
        payload["query"] = query

    if text_max_characters > 0:
        payload["textMaxCharacters"] = text_max_characters

    return await _make_request("crawl", payload)


@mcp.tool()
async def web_search_advanced_exa(
    query: str,
    num_results: int = 10,
    search_type: str = "auto",
    category: str = "",
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    include_text: list[str] | None = None,
    exclude_text: list[str] | None = None,
    start_published_date: str = "",
    end_published_date: str = "",
    enable_summary: bool = False,
    summary_query: str = "",
    enable_highlights: bool = False,
    highlights_query: str = "",
) -> dict[str, Any]:
    """Advanced web search with full control over filters, domains, dates, and content options.

    Args:
        query: The search query string.
        num_results: Number of results to return (default: 10).
        search_type: Search type - "auto", "fast", "deep", or "neural" (default: "auto").
        category: Category filter - "company", "news", "people", "research paper", "financial report", "personal site".
        include_domains: List of domains to include.
        exclude_domains: List of domains to exclude.
        include_text: List of text patterns that must be present (single item recommended).
        exclude_text: List of text patterns to exclude (single item recommended).
        start_published_date: Start date filter (ISO 8601 format, e.g., "2024-01-01").
        end_published_date: End date filter (ISO 8601 format).
        enable_summary: Enable AI-generated summary.
        summary_query: Query to guide summary generation.
        enable_highlights: Enable highlights extraction.
        highlights_query: Query to extract highlights.

    Returns:
        Dictionary containing advanced search results.

    Example:
        >>> web_search_advanced_exa(
        ...     query="AI infrastructure startups",
        ...     category="company",
        ...     num_results=20,
        ...     search_type="auto"
        ... )
        {"results": [...]}
    """
    if not query or not query.strip():
        return {"results": [], "message": "Query cannot be empty"}

    payload: dict[str, Any] = {
        "query": query,
        "numResults": num_results,
        "type": search_type,
    }

    if category:
        payload["category"] = category

    if include_domains:
        payload["includeDomains"] = include_domains

    if exclude_domains:
        payload["excludeDomains"] = exclude_domains

    if include_text:
        payload["includeText"] = include_text

    if exclude_text:
        payload["excludeText"] = exclude_text

    if start_published_date:
        payload["startPublishedDate"] = start_published_date

    if end_published_date:
        payload["endPublishedDate"] = end_published_date

    if enable_summary:
        payload["enableSummary"] = True
        if summary_query:
            payload["summaryQuery"] = summary_query

    if enable_highlights:
        payload["enableHighlights"] = True
        if highlights_query:
            payload["highlightsQuery"] = highlights_query

    return await _make_request("search", payload)

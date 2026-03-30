"""MCP server implementation for Exa websearch API."""

import os
from typing import Any, Literal, Union

import fastmcp
from exa_py import Exa
from pydantic import BaseModel

mcp = fastmcp.FastMCP("mcp-exa")


def get_exa_client() -> Exa:
    """Get an Exa client instance.

    Returns:
        Exa: An authenticated Exa client.

    Raises:
        ValueError: If the EXA_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise ValueError(
            "EXA_API_KEY environment variable is not set. "
            "Please set it before using the MCP server."
        )
    return Exa(api_key=api_key)


ContentsOptions = Union[dict[str, Any], Literal[False]]
SearchType = Literal["auto", "fast", "deep", "deep-reasoning", "instant"]
Category = Literal[
    "company",
    "news",
    "research_paper",
    "pdf",
    "github",
    "hackernews",
    "video",
    "image",
]
ResearchModel = Literal["exa-research-fast", "exa-research", "exa-research-pro"]
JSONSchemaInput = dict[str, Any]


@mcp.tool()
def search(
    query: str,
    num_results: int | None = None,
    contents: ContentsOptions | None = None,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    start_crawl_date: str | None = None,
    end_crawl_date: str | None = None,
    start_published_date: str | None = None,
    end_published_date: str | None = None,
    include_text: list[str] | None = None,
    exclude_text: list[str] | None = None,
    type: SearchType | None = None,
    category: Category | None = None,
    flags: list[str] | None = None,
    moderation: bool | None = None,
    user_location: str | None = None,
    additional_queries: list[str] | None = None,
    output_schema: JSONSchemaInput | None = None,
) -> dict[str, Any]:
    """Perform a web search using Exa.

    Args:
        query: The search query string.
        num_results: Number of search results to return (default: 10).
        contents: Options for retrieving page contents. Use False to disable.
        include_domains: Domains to include in the search.
        exclude_domains: Domains to exclude from the search.
        start_crawl_date: Only links crawled after this date (YYYY-MM-DD).
        end_crawl_date: Only links crawled before this date (YYYY-MM-DD).
        start_published_date: Only links published after this date (YYYY-MM-DD).
        end_published_date: Only links published before this date (YYYY-MM-DD).
        include_text: Strings that must appear in the page text.
        exclude_text: Strings that must not appear in the page text.
        type: Search type - 'auto', 'fast', 'deep', 'deep-reasoning', or 'instant'.
        category: Data category to focus on (e.g., 'company', 'news', 'research_paper').
        flags: Experimental flags for Exa usage.
        moderation: If True, moderate search results for safety.
        user_location: Two-letter ISO country code for user location.
        additional_queries: Alternative query formulations for deep search.
        output_schema: JSON schema for deep search structured output.

    Returns:
        Dict containing search results with optional contents.

    Example:
        >>> search("hottest AI startups", num_results=5)
        {"results": [{"title": "...", "url": "..."}]}
    """
    if not query:
        raise ValueError("Query cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if num_results is not None:
        kwargs["num_results"] = num_results
    if contents is not None:
        kwargs["contents"] = contents
    if include_domains is not None:
        kwargs["include_domains"] = include_domains
    if exclude_domains is not None:
        kwargs["exclude_domains"] = exclude_domains
    if start_crawl_date is not None:
        kwargs["start_crawl_date"] = start_crawl_date
    if end_crawl_date is not None:
        kwargs["end_crawl_date"] = end_crawl_date
    if start_published_date is not None:
        kwargs["start_published_date"] = start_published_date
    if end_published_date is not None:
        kwargs["end_published_date"] = end_published_date
    if include_text is not None:
        kwargs["include_text"] = include_text
    if exclude_text is not None:
        kwargs["exclude_text"] = exclude_text
    if type is not None:
        kwargs["type"] = type
    if category is not None:
        kwargs["category"] = category
    if flags is not None:
        kwargs["flags"] = flags
    if moderation is not None:
        kwargs["moderation"] = moderation
    if user_location is not None:
        kwargs["user_location"] = user_location
    if additional_queries is not None:
        kwargs["additional_queries"] = additional_queries
    if output_schema is not None:
        kwargs["output_schema"] = output_schema

    try:
        result = exa.search(query, **kwargs)
        return {"results": result.results}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def find_similar(
    url: str,
    num_results: int | None = None,
    contents: ContentsOptions | None = None,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    start_crawl_date: str | None = None,
    end_crawl_date: str | None = None,
    start_published_date: str | None = None,
    end_published_date: str | None = None,
    include_text: list[str] | None = None,
    exclude_text: list[str] | None = None,
    exclude_source_domain: bool | None = None,
    category: Category | None = None,
    flags: list[str] | None = None,
) -> dict[str, Any]:
    """Find pages similar to a given URL using Exa.

    Args:
        url: The URL to find similar pages for.
        num_results: Number of results to return.
        contents: Options for retrieving page contents. Use False to disable.
        include_domains: Domains to include in the search.
        exclude_domains: Domains to exclude from the search.
        start_crawl_date: Only links crawled after this date (YYYY-MM-DD).
        end_crawl_date: Only links crawled before this date (YYYY-MM-DD).
        start_published_date: Only links published after this date (YYYY-MM-DD).
        end_published_date: Only links published before this date (YYYY-MM-DD).
        include_text: Strings that must appear in the page text.
        exclude_text: Strings that must not appear in the page text.
        exclude_source_domain: Whether to exclude the source domain.
        category: Data category to focus on.
        flags: Experimental flags for Exa usage.

    Returns:
        Dict containing similar pages.

    Example:
        >>> find_similar("https://example.com", num_results=5)
        {"results": [{"title": "...", "url": "..."}]}
    """
    if not url:
        raise ValueError("URL cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if num_results is not None:
        kwargs["num_results"] = num_results
    if contents is not None:
        kwargs["contents"] = contents
    if include_domains is not None:
        kwargs["include_domains"] = include_domains
    if exclude_domains is not None:
        kwargs["exclude_domains"] = exclude_domains
    if start_crawl_date is not None:
        kwargs["start_crawl_date"] = start_crawl_date
    if end_crawl_date is not None:
        kwargs["end_crawl_date"] = end_crawl_date
    if start_published_date is not None:
        kwargs["start_published_date"] = start_published_date
    if end_published_date is not None:
        kwargs["end_published_date"] = end_published_date
    if include_text is not None:
        kwargs["include_text"] = include_text
    if exclude_text is not None:
        kwargs["exclude_text"] = exclude_text
    if exclude_source_domain is not None:
        kwargs["exclude_source_domain"] = exclude_source_domain
    if category is not None:
        kwargs["category"] = category
    if flags is not None:
        kwargs["flags"] = flags

    try:
        result = exa.find_similar(url, **kwargs)
        return {"results": result.results}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_contents(urls: str | list[str]) -> dict[str, Any]:
    """Retrieve contents for a list of URLs using Exa.

    Args:
        urls: A single URL or list of URLs to retrieve contents from.

    Returns:
        Dict containing the contents of each URL.

    Example:
        >>> get_contents(["https://example.com/article1", "https://example.com/article2"])
        {"results": [{"url": "...", "title": "...", "text": "..."}]}
    """
    if not urls:
        raise ValueError("URLs cannot be empty")

    if isinstance(urls, str):
        urls = [urls]

    exa = get_exa_client()

    try:
        result = exa.get_contents(urls)
        return {"results": result.results}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def answer(
    query: str,
    text: bool | None = None,
    system_prompt: str | None = None,
    model: Literal["exa"] | None = None,
    output_schema: JSONSchemaInput | None = None,
    user_location: str | None = None,
) -> dict[str, Any]:
    """Generate an answer to a query using Exa's search and LLM capabilities.

    Args:
        query: The query to answer.
        text: Whether to include full text in the results.
        system_prompt: A system prompt to guide the LLM's behavior.
        model: The model to use for answering (default: exa).
        output_schema: JSON schema for structured output.
        user_location: Two-letter ISO country code for user location.

    Returns:
        Dict containing the answer and citations.

    Example:
        >>> answer("What is the capital of France?")
        {"answer": "Paris", "citations": [...]}
    """
    if not query:
        raise ValueError("Query cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if text is not None:
        kwargs["text"] = text
    if system_prompt is not None:
        kwargs["system_prompt"] = system_prompt
    if model is not None:
        kwargs["model"] = model
    if output_schema is not None:
        kwargs["output_schema"] = output_schema
    if user_location is not None:
        kwargs["user_location"] = user_location

    try:
        result = exa.answer(query, **kwargs)
        return {
            "answer": result.answer,  # type: ignore[union-attr]
            "citations": [
                {
                    "id": c.id,
                    "url": c.url,
                    "title": c.title,
                    "published_date": c.published_date,
                    "author": c.author,
                    "text": c.text,
                }
                for c in result.citations  # type: ignore[union-attr]
            ]
            if result.citations  # type: ignore[union-attr]
            else [],
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def stream_answer(
    query: str,
    text: bool | None = None,
    system_prompt: str | None = None,
    model: Literal["exa"] | None = None,
    output_schema: JSONSchemaInput | None = None,
    user_location: str | None = None,
) -> list[dict[str, Any]]:
    """Generate a streaming answer response using Exa.

    Args:
        query: The query to answer.
        text: Whether to include full text in the results.
        system_prompt: A system prompt to guide the LLM's behavior.
        model: The model to use for answering.
        output_schema: JSON schema for structured output.
        user_location: Two-letter ISO country code for user location.

    Returns:
        List of dicts containing partial answers and citations.

    Example:
        >>> await stream_answer("What is the capital of France?")
        [{"content": "Paris", "citations": [...]}]
    """
    if not query:
        raise ValueError("Query cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if text is not None:
        kwargs["text"] = text
    if system_prompt is not None:
        kwargs["system_prompt"] = system_prompt
    if model is not None:
        kwargs["model"] = model
    if output_schema is not None:
        kwargs["output_schema"] = output_schema
    if user_location is not None:
        kwargs["user_location"] = user_location

    try:
        stream = exa.stream_answer(query, **kwargs)
        results = []
        async for chunk in stream:  # type: ignore[attr-defined]
            results.append(
                {
                    "content": chunk.content,
                    "citations": [
                        {
                            "id": c.id,
                            "url": c.url,
                            "title": c.title,
                            "published_date": c.published_date,
                            "author": c.author,
                            "text": c.text,
                        }
                        for c in (chunk.citations or [])
                    ],
                }
            )
        return results
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def research_create(
    instructions: str,
    model: ResearchModel | None = None,
    output_schema: JSONSchemaInput | None = None,
) -> dict[str, Any]:
    """Create a new research request using Exa.

    Args:
        instructions: The research instructions describing what to research.
        model: The model to use ('exa-research-fast', 'exa-research', 'exa-research-pro').
        output_schema: JSON schema for structured output format.

    Returns:
        Dict containing the research task ID and initial status.

    Example:
        >>> research_create(instructions="What is the latest valuation of SpaceX?")
        {"research_id": "abc-123", "status": "running"}
    """
    if not instructions:
        raise ValueError("Instructions cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if model is not None:
        kwargs["model"] = model
    if output_schema is not None:
        kwargs["output_schema"] = output_schema

    try:
        result = exa.research.create(instructions=instructions, **kwargs)
        return {
            "research_id": result.research_id,
            "status": result.status,
            "created_at": result.created_at,
            "model": result.model,
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def research_get(
    research_id: str,
    events: bool | None = None,
    output_schema: type[BaseModel] | None = None,
) -> dict[str, Any]:
    """Get a research request by ID using Exa.

    Args:
        research_id: The unique identifier of the research task.
        events: Whether to include events in the response.
        output_schema: Optional Pydantic model for typed output validation.

    Returns:
        Dict containing the research task status and output.

    Example:
        >>> research_get("abc-123")
        {"research_id": "abc-123", "status": "completed", "output": {...}}
    """
    if not research_id:
        raise ValueError("Research ID cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if events is not None:
        kwargs["events"] = events
    if output_schema is not None:
        kwargs["output_schema"] = output_schema

    try:
        result = exa.research.get(research_id, **kwargs)
        return {
            "research_id": result.research_id,
            "status": result.status,
            "created_at": result.created_at,
            "finished_at": result.finished_at,
            "model": result.model,
            "output": result.output,
            "cost_dollars": (
                {
                    "neural": result.cost_dollars.neural,
                    "keyword": result.cost_dollars.keyword,
                }
                if result.cost_dollars
                else None
            ),
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def research_poll_until_finished(
    research_id: str,
    poll_interval: int | None = None,
    timeout_ms: int | None = None,
    events: bool | None = None,
    output_schema: type[BaseModel] | None = None,
) -> dict[str, Any]:
    """Poll until research is finished using Exa.

    Args:
        research_id: The unique identifier of the research task.
        poll_interval: Milliseconds between polling attempts (default: 1000).
        timeout_ms: Maximum time to wait in milliseconds (default: 600000).
        events: Whether to include events in the response.
        output_schema: Optional Pydantic model for typed output validation.

    Returns:
        Dict containing the completed research task.

    Example:
        >>> research_poll_until_finished("abc-123")
        {"research_id": "abc-123", "status": "completed", "output": {...}}
    """
    if not research_id:
        raise ValueError("Research ID cannot be empty")

    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if poll_interval is not None:
        kwargs["poll_interval"] = poll_interval
    if timeout_ms is not None:
        kwargs["timeout_ms"] = timeout_ms
    if events is not None:
        kwargs["events"] = events
    if output_schema is not None:
        kwargs["output_schema"] = output_schema

    try:
        result = exa.research.poll_until_finished(research_id, **kwargs)
        return {
            "research_id": result.research_id,
            "status": result.status,
            "created_at": result.created_at,
            "finished_at": result.finished_at,
            "model": result.model,
            "output": result.output,
            "cost_dollars": (
                {
                    "neural": result.cost_dollars.neural,
                    "keyword": result.cost_dollars.keyword,
                }
                if result.cost_dollars
                else None
            ),
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def research_list(
    cursor: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """List research requests using Exa.

    Args:
        cursor: Pagination cursor from a previous response.
        limit: Maximum number of results to return.

    Returns:
        Dict containing the list of research requests.

    Example:
        >>> research_list(limit=10)
        {"data": [...], "has_more": true, "next_cursor": "..."}
    """
    exa = get_exa_client()

    kwargs: dict[str, Any] = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit

    try:
        result = exa.research.list(**kwargs)
        return {
            "data": [
                {
                    "id": r.id,  # type: ignore[union-attr]
                    "status": r.status,
                    "instructions": r.instructions,
                    "created_at": r.created_at,
                    "model": r.model,
                }
                for r in result.data
            ],
            "has_more": result.has_more,
            "next_cursor": result.next_cursor,
        }
    except Exception as e:
        return {"error": str(e)}

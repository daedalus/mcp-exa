"""MCP server implementation for Exa websearch API - uses public MCP endpoint."""

import uuid
from typing import Any, Literal, Union

import fastmcp
import httpx
from pydantic import BaseModel

mcp = fastmcp.FastMCP("mcp-exa")

BASE_URL = "https://mcp.exa.ai"

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


async def _call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Call a tool on the public Exa MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/mcp",
            json=request,
            headers={
                "accept": "application/json, text/event-stream",
                "content-type": "application/json",
            },
        )
        response.raise_for_status()
        response_text = response.text

        lines = response_text.split("\n")
        for line in lines:
            if line.startswith("data: "):
                data = line[6:]
                result = {"jsonrpc": "2.0", "id": 1, "result": {}}
                try:
                    parsed = eval(data)
                except Exception:
                    pass
                else:
                    if "result" in parsed and parsed["result"].get("content"):
                        return {
                            "results": parsed["result"]["content"][0].get("text", "")
                        }

        return {"results": ""}


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
    import asyncio

    if not query:
        raise ValueError("Query cannot be empty")

    arguments: dict[str, Any] = {"query": query}
    if num_results is not None:
        arguments["numResults"] = num_results
    if contents is not None:
        arguments["contents"] = contents
    if include_domains is not None:
        arguments["include_domains"] = include_domains
    if exclude_domains is not None:
        arguments["exclude_domains"] = exclude_domains
    if start_crawl_date is not None:
        arguments["start_crawl_date"] = start_crawl_date
    if end_crawl_date is not None:
        arguments["end_crawl_date"] = end_crawl_date
    if start_published_date is not None:
        arguments["start_published_date"] = start_published_date
    if end_published_date is not None:
        arguments["end_published_date"] = end_published_date
    if include_text is not None:
        arguments["include_text"] = include_text
    if exclude_text is not None:
        arguments["exclude_text"] = exclude_text
    if type is not None:
        arguments["type"] = type
    if category is not None:
        arguments["category"] = category
    if flags is not None:
        arguments["flags"] = flags
    if moderation is not None:
        arguments["moderation"] = moderation
    if user_location is not None:
        arguments["user_location"] = user_location
    if additional_queries is not None:
        arguments["additional_queries"] = additional_queries
    if output_schema is not None:
        arguments["output_schema"] = output_schema

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("web_search_exa", arguments)
        )
        return result
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
    import asyncio

    if not url:
        raise ValueError("URL cannot be empty")

    arguments: dict[str, Any] = {"url": url}
    if num_results is not None:
        arguments["numResults"] = num_results
    if contents is not None:
        arguments["contents"] = contents
    if include_domains is not None:
        arguments["include_domains"] = include_domains
    if exclude_domains is not None:
        arguments["exclude_domains"] = exclude_domains
    if start_crawl_date is not None:
        arguments["start_crawl_date"] = start_crawl_date
    if end_crawl_date is not None:
        arguments["end_crawl_date"] = end_crawl_date
    if start_published_date is not None:
        arguments["start_published_date"] = start_published_date
    if end_published_date is not None:
        arguments["end_published_date"] = end_published_date
    if include_text is not None:
        arguments["include_text"] = include_text
    if exclude_text is not None:
        arguments["exclude_text"] = exclude_text
    if exclude_source_domain is not None:
        arguments["exclude_source_domain"] = exclude_source_domain
    if category is not None:
        arguments["category"] = category
    if flags is not None:
        arguments["flags"] = flags

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_find_similar", arguments)
        )
        return result
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
    import asyncio

    if not urls:
        raise ValueError("URLs cannot be empty")

    if isinstance(urls, str):
        urls = [urls]

    arguments: dict[str, Any] = {"urls": urls}

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_get_contents", arguments)
        )
        return result
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
    import asyncio

    if not query:
        raise ValueError("Query cannot be empty")

    arguments: dict[str, Any] = {"query": query}
    if text is not None:
        arguments["text"] = text
    if system_prompt is not None:
        arguments["system_prompt"] = system_prompt
    if model is not None:
        arguments["model"] = model
    if output_schema is not None:
        arguments["output_schema"] = output_schema
    if user_location is not None:
        arguments["user_location"] = user_location

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_answer", arguments)
        )
        return result
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

    arguments: dict[str, Any] = {"query": query}
    if text is not None:
        arguments["text"] = text
    if system_prompt is not None:
        arguments["system_prompt"] = system_prompt
    if model is not None:
        arguments["model"] = model
    if output_schema is not None:
        arguments["output_schema"] = output_schema
    if user_location is not None:
        arguments["user_location"] = user_location

    try:
        result = await _call_mcp_tool("exa_stream_answer", arguments)
        return [result]
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
    import asyncio

    if not instructions:
        raise ValueError("Instructions cannot be empty")

    arguments: dict[str, Any] = {"instructions": instructions}
    if model is not None:
        arguments["model"] = model
    if output_schema is not None:
        arguments["output_schema"] = output_schema

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_research_create", arguments)
        )
        return result
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
    import asyncio

    if not research_id:
        raise ValueError("Research ID cannot be empty")

    arguments: dict[str, Any] = {"research_id": research_id}
    if events is not None:
        arguments["events"] = events
    if output_schema is not None:
        arguments["output_schema"] = output_schema

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_research_get", arguments)
        )
        return result
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
    import asyncio

    if not research_id:
        raise ValueError("Research ID cannot be empty")

    arguments: dict[str, Any] = {"research_id": research_id}
    if poll_interval is not None:
        arguments["poll_interval"] = poll_interval
    if timeout_ms is not None:
        arguments["timeout_ms"] = timeout_ms
    if events is not None:
        arguments["events"] = events
    if output_schema is not None:
        arguments["output_schema"] = output_schema

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_research_poll_until_finished", arguments)
        )
        return result
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
    import asyncio

    arguments: dict[str, Any] = {}
    if cursor is not None:
        arguments["cursor"] = cursor
    if limit is not None:
        arguments["limit"] = limit

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _call_mcp_tool("exa_research_list", arguments)
        )
        return result
    except Exception as e:
        return {"error": str(e)}

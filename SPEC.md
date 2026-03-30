# SPEC.md — mcp-exa

## Purpose

An MCP (Model Context Protocol) server that exposes all Exa websearch API methods as tools, enabling LLMs to perform web searches, find similar pages, retrieve contents, and conduct research tasks.

## Scope

- **In scope:**
  - Exa `search` method as MCP tool
  - Exa `find_similar` method as MCP tool
  - Exa `get_contents` method as MCP tool
  - Exa `answer` method as MCP tool
  - Exa `stream_answer` method as MCP tool (async)
  - Exa `research.create` method as MCP tool
  - Exa `research.get` method as MCP tool
  - Exa `research.poll_until_finished` method as MCP tool
  - Exa `research.list` method as MCP tool
  - Proper error handling with meaningful messages
  - Environment variable API key management

- **Not in scope:**
  - Custom authentication schemes beyond EXA_API_KEY
  - Rate limiting implementation (handled by Exa API)
  - Caching of results

## Public API / Interface

### MCP Tools

All tools follow the pattern `@mcp.tool()` and are exposed via stdio transport.

#### `search`

```python
def search(
    query: str,
    num_results: Optional[int] = None,
    contents: Optional[Union[ContentsOptions, Literal[False]]] = None,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
    start_crawl_date: Optional[str] = None,
    end_crawl_date: Optional[str] = None,
    start_published_date: Optional[str] = None,
    end_published_date: Optional[str] = None,
    include_text: Optional[List[str]] = None,
    exclude_text: Optional[List[str]] = None,
    type: Optional[Union[SearchType, str]] = None,
    category: Optional[Category] = None,
    flags: Optional[List[str]] = None,
    moderation: Optional[bool] = None,
    user_location: Optional[str] = None,
    additional_queries: Optional[List[str]] = None,
    output_schema: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]
```

Performs a web search and returns results with optional contents.

#### `find_similar`

```python
def find_similar(
    url: str,
    num_results: Optional[int] = None,
    contents: Optional[Union[ContentsOptions, Literal[False]]] = None,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
    start_crawl_date: Optional[str] = None,
    end_crawl_date: Optional[str] = None,
    start_published_date: Optional[str] = None,
    end_published_date: Optional[str] = None,
    include_text: Optional[List[str]] = None,
    exclude_text: Optional[List[str]] = None,
    exclude_source_domain: Optional[bool] = None,
    category: Optional[Category] = None,
    flags: Optional[List[str]] = None,
) -> Dict[str, Any]
```

Finds pages similar to a given URL.

#### `get_contents`

```python
def get_contents(
    urls: Union[str, List[str], List[Result]],
) -> Dict[str, Any]
```

Retrieves contents for a list of URLs.

#### `answer`

```python
def answer(
    query: str,
    text: Optional[bool] = None,
    system_prompt: Optional[str] = None,
    model: Optional[Literal["exa"]] = None,
    output_schema: Optional[JSONSchemaInput] = None,
    user_location: Optional[str] = None,
) -> Dict[str, Any]
```

Generates an answer to a query using Exa's search and LLM capabilities.

#### `stream_answer`

```python
async def stream_answer(
    query: str,
    text: Optional[bool] = None,
    system_prompt: Optional[str] = None,
    model: Optional[Literal["exa"]] = None,
    output_schema: Optional[JSONSchemaInput] = None,
    user_location: Optional[str] = None,
) -> AsyncIterator[Dict[str, Any]]
```

Generates a streaming answer response.

#### `research_create`

```python
def research_create(
    instructions: str,
    model: Optional[ResearchModel] = None,
    output_schema: Optional[Union[Dict[str, Any], Type[BaseModel]]] = None,
) -> Dict[str, Any]
```

Creates a new research request.

#### `research_get`

```python
def research_get(
    research_id: str,
    events: Optional[bool] = None,
    output_schema: Optional[Type[BaseModel]] = None,
) -> Dict[str, Any]
```

Gets a research request by ID.

#### `research_poll_until_finished`

```python
def research_poll_until_finished(
    research_id: str,
    poll_interval: Optional[int] = None,
    timeout_ms: Optional[int] = None,
    events: Optional[bool] = None,
    output_schema: Optional[Type[BaseModel]] = None,
) -> Dict[str, Any]
```

Polls until research is finished.

#### `research_list`

```python
def research_list(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]
```

Lists research requests.

## Data Formats

### Input Types

- `ContentsOptions`: Dict with text, highlights, summary, context, max_age_hours, subpages, subpage_target, extras
- `SearchType`: "auto", "fast", "deep", "deep-reasoning", "instant"
- `Category`: "company", "news", "research_paper", "pdf", "github", "hackernews", "video", "image"
- `ResearchModel`: "exa-research-fast", "exa-research", "exa-research-pro"
- `JSONSchemaInput`: Dict or Pydantic model for structured output

### Output Formats

All tools return `Dict[str, Any]` containing the Exa API response.

## Edge Cases

1. **Missing API key**: Raise `ValueError` with clear message about EXA_API_KEY
2. **Empty query**: Raise `ValueError` for empty search queries
3. **Invalid URL for find_similar**: Raise `ValueError` for malformed URLs
4. **Empty URL list for get_contents**: Raise `ValueError` for empty URL list
5. **Research timeout**: Handle timeout in poll_until_finished with clear message
6. **Network errors**: Wrap in try/except and provide meaningful error messages
7. **Invalid output schema**: Validate and provide clear error messages

## Performance & Constraints

- All synchronous tools must complete within 120 seconds (MCP default timeout)
- Async streaming tools should yield results as they arrive
- Memory usage should be proportional to number of results
- Use type hints throughout for mypy compatibility

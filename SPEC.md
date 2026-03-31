# SPEC.md — mcp-exa

## Purpose

A Python MCP server that exposes the Exa (https://mcp.exa.ai/mcp) search API as MCP tools. This allows AI assistants to access Exa's web search, code search, and web crawling capabilities through the Model Context Protocol.

## Scope

### What IS in scope
- MCP server implementation using FastMCP
- Four main tools: web_search, get_code_context, crawling, web_search_advanced
- Support for Exa API key authentication via environment variable
- HTTP transport support for remote deployment
- Proper error handling and validation

### What is NOT in scope
- Hosting the server (users deploy their own)
- Caching or rate limiting (delegate to Exa API)
- Authentication beyond Exa API key

## Public API / Interface

### MCP Tools

1. **web_search_exa**
   - Args:
     - `query` (str, required): Search query
     - `numResults` (int, optional): Number of results (default: 10)
     - `textMaxCharacters` (int, optional): Max characters per result
     - `summaryQuery` (str, optional): Query to summarize results
   - Returns: List of search results with title, url, content

2. **get_code_context_exa**
   - Args:
     - `query` (str, required): Code search query
     - `tokensNum` (int, optional): Context length (default: 5000)
   - Returns: Code examples with source URLs

3. **crawling_exa**
   - Args:
     - `url` (str, required): URL to crawl
     - `query` (str, optional): Query to extract relevant content
     - `textMaxCharacters` (int, optional): Max characters
   - Returns: Extracted content from the URL

4. **web_search_advanced_exa**
   - Args:
     - `query` (str, required): Search query
     - `numResults` (int, optional): Number of results
     - `type` (str, optional): Search type ("auto", "fast", "deep", "neural")
     - `category` (str, optional): Category filter
     - `includeDomains` (list[str], optional): Domains to include
     - `excludeDomains` (list[str], optional): Domains to exclude
     - `includeText` (list[str], optional): Text must contain
     - `excludeText` (list[str], optional): Text must not contain
     - `startPublishedDate` (str, optional): ISO date string
     - `endPublishedDate` (str, optional): ISO date string
     - `enableSummary` (bool, optional): Enable AI summary
     - `summaryQuery` (str, optional): Query for summary
     - `enableHighlights` (bool, optional): Enable highlights
     - `highlightsQuery` (str, optional): Query for highlights
   - Returns: Advanced search results

## Data Formats

- All API calls use JSON over HTTPS
- API key passed via `EXA_API_KEY` environment variable
- Results returned as structured JSON

## Edge Cases

1. Missing API key → Raise helpful error message
2. Invalid query → Return empty results with message
3. API rate limit → Propagate error with retry suggestion
4. Network failure → Raise connection error
5. Invalid URL for crawling → Return error message

## Performance & Constraints

- Use httpx for async HTTP requests
- Default timeout: 30 seconds
- Respect API limits from Exa

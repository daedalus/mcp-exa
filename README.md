# mcp-exa

> MCP server exposing Exa websearch API

[![PyPI](https://img.shields.io/pypi/v/mcp-exa.svg)](https://pypi.org/project/mcp-exa/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-exa.svg)](https://pypi.org/project/mcp-exa/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

mcp-name: io.github.daedalus/mcp-exa

## Install

```bash
pip install mcp-exa
```

## Usage

### Set up your API key

```bash
export EXA_API_KEY="your-api-key"
```

### Run as MCP server

```bash
mcp-exa
```

### Available Tools

The MCP server exposes the following Exa API methods as tools:

- `search` - Perform a web search
- `find_similar` - Find pages similar to a URL
- `get_contents` - Retrieve contents for URLs
- `answer` - Generate an answer using Exa's LLM capabilities
- `stream_answer` - Stream an answer response
- `research_create` - Create a research task
- `research_get` - Get a research task by ID
- `research_poll_until_finished` - Poll until research completes
- `research_list` - List research tasks

## Development

```bash
git clone https://github.com/daedalus/mcp-exa.git
cd mcp-exa
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

# MCP Exa

> A Python MCP server that exposes Exa search capabilities (no API key required)

[![PyPI](https://img.shields.io/pypi/v/mcp-exa.svg)](https://pypi.org/project/mcp-exa/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-exa.svg)](https://pypi.org/project/mcp-exa/)
[![Coverage](https://codecov.io/gh/daedalus/mcp-exa/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/mcp-exa)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

mcp-name: io.github.daedalus/mcp-exa

## Install

```bash
pip install mcp-exa
```

## Usage

No API key required. The server uses Exa's public MCP endpoint.

Run the MCP server:

```bash
mcp-exa
```

Or use as a module:

```bash
python -m mcp_exa
```

## Configuration

### Available Tools

The server exposes the following MCP tools:

| Tool | Description |
| ---- | ----------- |
| `web_search_exa` | Search the web for any topic |
| `get_code_context_exa` | Find code examples from GitHub, Stack Overflow |
| `crawling_exa` | Get full content from a specific URL |
| `web_search_advanced_exa` | Advanced search with filters |

## MCP Client Configuration

### Claude Desktop

Add to your config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "exa": {
      "command": "mcp-exa"
    }
  }
}
```

### OpenCode

Add to your `opencode.json`:

```json
{
  "mcp": {
    "exa": {
      "type": "stdio",
      "command": "mcp-exa",
      "enabled": true
    }
  }
}
```

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

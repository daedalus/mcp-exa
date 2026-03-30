"""MCP server for Exa websearch API."""

__version__ = "0.1.0"
__all__ = ["mcp", "get_exa_client"]

from ._server import get_exa_client, mcp

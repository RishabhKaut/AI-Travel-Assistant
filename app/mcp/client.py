"""
MCP client wiring: connects to app/mcp/server.py over stdio using
langchain-mcp-adapters, and exposes the resulting tools (get_weather_forecast,
convert_currency) as ordinary LangChain Tool objects that a LangGraph/LangChain
agent can call like any other tool.

Using MultiServerMCPClient (rather than importing server.py's functions
directly) is what makes this an actual MCP integration: the server could be
swapped for a different weather/currency MCP server, or run remotely, without
changing the agent code at all.

The installed langchain-mcp-adapters version keeps the stdio subprocess and
session alive only while the MultiServerMCPClient's async context manager is
open, so for a long-running FastAPI server we open the connection once at
app startup (see the lifespan handler in app/main.py) and close it at
shutdown, rather than reconnecting on every request.
"""
from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_SCRIPT = str(Path(__file__).resolve().parent / "server.py")

_client: MultiServerMCPClient | None = None
_tools: list[BaseTool] | None = None


async def start_mcp_client() -> list[BaseTool]:
    """Opens the MCP connection (spawns the stdio server subprocess) and
    loads its tools. Call once at application startup."""
    global _client, _tools
    if _tools is not None:
        return _tools

    _client = MultiServerMCPClient(
        {
            "travel_current_info": {
                "command": sys.executable,
                "args": [SERVER_SCRIPT],
                "transport": "stdio",
            }
        }
    )
    await _client.__aenter__()
    _tools = _client.get_tools()
    return _tools


async def stop_mcp_client() -> None:
    """Closes the MCP connection. Call once at application shutdown."""
    global _client, _tools
    if _client is not None:
        await _client.__aexit__(None, None, None)
    _client = None
    _tools = None


def get_mcp_tools() -> list[BaseTool]:
    """Returns the already-loaded MCP tools (get_weather_forecast,
    convert_currency). Raises if start_mcp_client() has not run yet."""
    if _tools is None:
        raise RuntimeError(
            "MCP client not started. start_mcp_client() must be awaited "
            "during application startup before tools can be used."
        )
    return _tools

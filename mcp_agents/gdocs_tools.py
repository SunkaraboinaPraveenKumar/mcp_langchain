from mcp.server.fastmcp import mcp_tool

@mcp_tool()
def get_recent_docs(user: str) -> str:
    """Fetch recent Google Docs for the user (placeholder)."""
    return f"Fetched recent Google Docs for {user} (placeholder)." 
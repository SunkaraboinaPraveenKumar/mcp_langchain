from mcp.server.fastmcp import mcp_tool

@mcp_tool()
def get_recent_slides(user: str) -> str:
    """Fetch recent Google Slides for the user (placeholder)."""
    return f"Fetched recent Google Slides for {user} (placeholder)." 
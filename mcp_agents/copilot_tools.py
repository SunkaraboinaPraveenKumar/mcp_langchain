from mcp.server.fastmcp import mcp_tool

@mcp_tool()
def ask_question(question: str) -> str:
    """Answer user questions by calling other tools (placeholder)."""
    return f"This is a placeholder answer for: {question}" 
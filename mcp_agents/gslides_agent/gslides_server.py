from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("GSlidesAgent")

@mcp.tool()
def get_recent_slides(user: str) -> str:
    """Fetch recent Google Slides for the user (placeholder)."""
    return f"Fetched recent Google Slides for {user} (placeholder)."

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 
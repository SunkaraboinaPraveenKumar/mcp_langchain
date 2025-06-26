from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("GCalAgent")

@mcp.tool()
def get_upcoming_events(user: str) -> str:
    """Fetch upcoming calendar events for the user (placeholder)."""
    return f"Fetched upcoming events for {user} (placeholder)."

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 
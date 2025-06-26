from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("GDocsAgent")

@mcp.tool()
def get_recent_docs(user: str) -> str:
    """Fetch recent Google Docs for the user (placeholder)."""
    return f"Fetched recent Google Docs for {user} (placeholder)."

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 
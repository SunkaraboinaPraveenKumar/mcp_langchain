from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("GmailAgent")

@mcp.tool()
def get_recent_emails(user: str) -> str:
    """Fetch recent emails for the user (placeholder)."""
    return f"Fetched recent emails for {user} (placeholder)."

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 
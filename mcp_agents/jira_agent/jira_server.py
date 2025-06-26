from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("JiraAgent")

@mcp.tool()
def get_ticket_details(ticket_id: str) -> str:
    """Fetch details for a JIRA ticket (placeholder)."""
    return f"Fetched details for JIRA ticket {ticket_id} (placeholder)."

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 
from mcp.server.fastmcp import mcp_tool

@mcp_tool()
def get_ticket_details(ticket_id: str) -> str:
    """Fetch details for a JIRA ticket (placeholder)."""
    return f"Fetched details for JIRA ticket {ticket_id} (placeholder)." 
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("CopilotChatbot")

@mcp.tool()
def ask_question(question: str) -> str:
    """Answer user questions by calling other agents (placeholder)."""
    return f"This is a placeholder answer for: {question}"

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import asyncio
import os

async def main():
    # Connect to the unified MCP server
    client = MultiServerMCPClient({
        "copilot": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http"
        }
    })

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    tools = await client.get_tools()

    model = ChatGroq(model="llama3-8b-8192")
    agent = create_react_agent(model, tools)

    print("Copilot is ready! Type your questions (Ctrl+C to exit):")
    while True:
        user_input = input("You: ")
        response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
        print("Copilot:", response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main()) 
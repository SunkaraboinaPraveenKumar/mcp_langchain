from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

import asyncio

async def main():
    print("Client: Initializing MultiServerMCPClient...")
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], ## Ensure correct absolute path,
                "transport":"stdio"
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp", ## Ensure server is running here
                "transport":"streamable_http"
            }
        }
    )

    # IMPORTANT: Ensure weather.py is running as a separate process (e.g., python weather.py) before running this client.

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    print("Client: Getting tools...")
    tools = await client.get_tools()
    print(f"Client: Found tools: {[tool.name for tool in tools]}")

    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(
        model,
        tools
    )

    # math_response = await agent.ainvoke(
    #     {"messages":[{"role":"user","content":"What's (3+5)x12?"}]}
    # )

    # print("Math Response:",math_response['messages'][-1].content)

    print("Client: Invoking weather agent...")
    weather_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"What's the weather like in Hyderabad?"}]}
    )

    print("Weather Response:",weather_response['messages'][-1].content)


asyncio.run(main())
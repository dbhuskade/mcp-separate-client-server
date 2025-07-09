from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import asyncio

from dotenv import load_dotenv
load_dotenv()

async def main():
    # create a MultiServerMCPClient instance with the servers you want to connect to
    client = MultiServerMCPClient(
        {
            # For local development, you can use the following servers
            # "math": {
            #     "command": "python",
            #     # Make sure to update to the full absolute path to your math_server.py file
            #     "args": ["mathserver.py"],
            #     "transport": "stdio",
            # },
            # "web-search": {
            #     "command": "python",
            #     # Make sure to update to the full absolute path to your math_server.py file
            #     "args": ["web_search.py"],
            #     "transport": "stdio",
            # },

            # for http transport, you can use the following servers
            "web-search": {
                # Make sure you start your weather server on port 10000
                "url": "http://localhost:10000/web/mcp/",
                "transport": "streamable_http",
            },
            "math": {
                # Make sure you start your weather server on port 10000
                "url": "http://localhost:10000/math/mcp/",
                "transport": "streamable_http",
            }
        }  # type: ignore
    )

    import os
    # Set the GROQ_API_KEY environment variable
    # Make sure to set the GROQ_API_KEY in your environment variables
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

    try:
        # Get the tools from the client
        # This will automatically connect to the servers and retrieve the tools
        tools = await client.get_tools()
    except Exception as ex:
        print("Error creating agent:", ex)
        return
    # You can change the model to any other model supported by Groq
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model=model, tools=tools)

    math_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    # Add you prompt here
                    # This is the prompt that will be sent to the agent
                    "content": "What is combined ODI centuries by Sachin Tendulkar and Virat Kohli?",
                }
            ]
        }
    )
    res = math_response["messages"][-1].content
    print("Response----->", res)

asyncio.run(main())

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
import asyncio

from dotenv import load_dotenv
load_dotenv()

async def main():
    # create a MultiServerMCPClient instance with the servers you want to connect to
    client = MultiServerMCPClient(
        {
            # for http transport, you can use the following servers
            "restaurant": {
                # Make sure you start your weather server on port 10000
                "url": "http://localhost:10000/restaurants/mcp/",
                "transport": "streamable_http",
            },
        }  # type: ignore
    )

    import os
    # Set the GROQ_API_KEY environment variable
    # Make sure to set the GROQ_API_KEY in your environment variables
    if "AZURE_OPENAI_API_KEY" not in os.environ:
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
    if "AZURE_OPENAI_ENDPOINT" not in os.environ:
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")

    try:
        # Get the tools from the client
        # This will automatically connect to the servers and retrieve the tools
        tools = await client.get_tools()
        prompts = await client.get_prompt(server_name='restaurant', prompt_name='greeting')
        # print("Prompts: ", prompts)
    except Exception as ex:
        print("Error creating agent:", ex)
        return
    # You can change the model to any other model supported by Groq
    az_oai = AzureChatOpenAI(
        azure_deployment="gpt-4o",  
        api_version="2025-01-01-preview",
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        )
    agent = create_react_agent(model=az_oai, tools=tools)
    # ------------------------
    # user_question = "Hi buddy, I'm Reenee."
    # user_question = "I'm hungry, what are some good restaurants available?"
    user_question = "Okay, tell me more about BellaZaika menu."
    #  ----------------------
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    # Add you prompt here
                    # This is the prompt that will be sent to the agent
                    "content": user_question,
                    # "content": "What Sushi Spot serves?",
                }
            ]
        }
    )
    res = response["messages"][-1].content
    print("User question: ",user_question)
    print("Response----->", res)

asyncio.run(main())

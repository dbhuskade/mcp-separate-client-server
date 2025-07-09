from mcp.server.fastmcp import FastMCP
from typing import Dict, List
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

if "TAVILY_API_KEY" not in os.environ:
    raise Exception("TAVILY_API_KEY is not in env file")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

tavily_client = TavilyClient(TAVILY_API_KEY)

mcp = FastMCP("WebSeach", host="0.0.0.0", port=8080)


@mcp.tool(description="Tool to search web")
def web_search(query: str) -> List[Dict]:
    """
    Use this tool to search the web.
    Args:
        query:  the search query
    Return:
        the search result.
    """
    try:
        response = tavily_client.search(query=query)
        return response["results"]
    except Exception as ex:
        return []


# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")

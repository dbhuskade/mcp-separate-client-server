from mcp.server.fastmcp import FastMCP

mcp =  FastMCP("math",port = 8070)

@mcp.tool()
def add(a:int,b:int)->int:
    """ To add two numbers
    """
    return a+b

@mcp.tool()
def multiply(a:int,b:int)->int:
    """Multiply numbers"""
    return a*b

# transport 'stdio' tells the client to interact with the math server with command line.
if __name__ == '__main__':
    print("Starting Math Server...")
    mcp.run(transport='stdio')
    print("Math Server is running. You can now send requests.")
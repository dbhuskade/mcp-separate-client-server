import contextlib
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mathserver import mcp as math_mcp
from web_search import mcp as web_search_mcp

# create a conbined lifespan to manage the lifespan of both MCP instances
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        # Register the math MCP instance
        await stack.enter_async_context(math_mcp.session_manager.run())
        # Register the web search MCP instance
        await stack.enter_async_context(web_search_mcp.session_manager.run())
        yield
#  create the FastAPI app with the combined lifespan
app = FastAPI(lifespan=lifespan)
# Mount the MCP instances to specific paths
app.mount("/math", math_mcp.streamable_http_app())
app.mount("/web", web_search_mcp.streamable_http_app())
# Add CORS middleware to allow requests from any origin
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

PORT = os.environ.get("PORT", 10000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(PORT), log_level="info")

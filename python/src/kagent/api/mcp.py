from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from typing import AsyncGenerator
import json
import asyncio

router = APIRouter()

async def event_generator(request: Request) -> AsyncGenerator[str, None]:
    while True:
        if await request.is_disconnected():
            break

        # Send tool information in JSON-RPC format
        message = {
            "jsonrpc": "2.0",
            "method": "tools.list",
            "params": {
                "tools": [
                    {
                        "name": "test-tool",
                        "component": {
                            "provider": "mcp",
                            "component_type": "tool",
                            "version": 1,
                            "component_version": 1,
                            "description": "A test tool",
                            "label": "Test Tool",
                            "config": {}
                        }
                    }
                ]
            },
            "id": 1
        }
        
        yield f"data: {json.dumps(message)}\n\n"
        
        # Send a heartbeat every 15 seconds
        await asyncio.sleep(15)
        yield "event: heartbeat\ndata: {}\n\n"

@router.get("/sse")
async def mcp_sse(request: Request) -> StreamingResponse:
    return EventSourceResponse(event_generator(request)) 

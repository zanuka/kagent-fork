from typing import Any
from autogen_core import CancellationToken
from autogen_core.tools import FunctionTool
from pydantic import BaseModel

class HelloInput(BaseModel):
    name: str = "World"

async def say_hello(args: HelloInput, cancellation_token: CancellationToken) -> str:
    return f"Hello, {args.name}!"

hello_tool = FunctionTool(
    say_hello,
    description="A simple tool that says hello",
    name="hello"
) 

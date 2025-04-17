from typing import Any, Dict, Optional
from .base import McpToolAdapter
import aiohttp
import asyncio
import json

class SseMcpToolAdapter(McpToolAdapter):
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None, timeout: float = 30.0):
        self.url = url
        self.headers = headers or {}
        self.timeout = timeout
        self.session = None

    async def connect(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def disconnect(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        await self.connect()
        
        try:
            async with self.session.get(
                self.url,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                response.raise_for_status()
                
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        if data.get('type') == 'result':
                            return data.get('payload', {})
                        
        except Exception as e:
            return {"error": str(e)}
        finally:
            await self.disconnect()

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "SseMcpToolAdapter":
        return cls(
            url=config["url"],
            headers=config.get("headers"),
            timeout=config.get("timeout", 30.0)
        )

    def to_config(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "headers": self.headers,
            "timeout": self.timeout
        } 

from kademlia.network import Server
import asyncio, json, os

BOOTSTRAP_PORT = 5678
class DHT:
    def __init__(self, port: int):
        self.port = port
        self.server = Server()

    async def start(self, bootstrap: str | None = None):
        await self.server.listen(self.port)
        if bootstrap:
            host, port = bootstrap.split(":")
            await self.server.bootstrap([(host, int(port))])
        else:
            # 첫 노드면 자신을 bootstrap으로
            await self.server.bootstrap([("127.0.0.1", self.port)])

    async def set(self, key: str, value: dict):
        await self.server.set(key, json.dumps(value))

    async def get(self, key: str) -> dict | None:
        raw = await self.server.get(key)
        return json.loads(raw) if raw else None

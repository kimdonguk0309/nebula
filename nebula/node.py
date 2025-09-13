import asyncio, pathlib, os, hashlib
from .protocol import NebulaProtocol
from .dht import DHT

class Node:
    def __init__(self, port: int, bootstrap: str | None = None):
        self.port = port
        self.proto = NebulaProtocol(port)
        self.dht  = DHT(port + 1000)
        self.bootstrap = bootstrap

    async def start(self):
        await self.dht.start(self.bootstrap)
        # apps/ 안의 .neb 파일들 자동 put
        for f in pathlib.Path("apps").glob("*.neb"):
            raw = f.read_bytes()
            h = hashlib.sha256(raw).hexdigest()
            self.proto.store[h] = raw
            await self.dht.set(f"neb:{f.stem}", {"hash": h})
            print(f"[NODE] {f.name} → {h}")
        await self.proto.start()

import socket, struct, lz4.frame, json, hashlib, asyncio

CHUNK = 64 * 1024
def _hash(b): return hashlib.sha256(b).hexdigest()

def pack(obj: dict) -> bytes:
    raw = json.dumps(obj).encode()
    return struct.pack(">I", len(raw)) + raw

async def unpack(reader: asyncio.StreamReader) -> dict:
    ln = struct.unpack(">I", await reader.readexactly(4))[0]
    return json.loads(await reader.readexactly(ln))

class NebulaProtocol:
    def __init__(self, port: int):
        self.port = port
        self.store: dict[str, bytes] = {}          # hash -> raw content

    async def handler(self, reader, writer):
        try:
            req = await unpack(reader)
            if req["op"] == "get":
                h = req["hash"]
                data = self.store.get(h, b"")
                writer.write(pack({"data": data.hex()}))
                await writer.drain()
            elif req["op"] == "put":
                raw = bytes.fromhex(req["data"])
                h = _hash(raw)
                self.store[h] = raw
                writer.write(pack({"status": "ok", "hash": h}))
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        srv = await asyncio.start_server(self.handler, "0.0.0.0", self.port)
        async with srv:
            await srv.serve_forever()

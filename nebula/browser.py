import tkinter as tk, tkinter.scrolledtext as st, asyncio, threading
from .protocol import pack, unpack
from .markup import parse

class Browser(tk.Tk):
    def __init__(self, node_port: int):
        super().__init__()
        self.node_port = node_port
        self.title("Nebula Browser")
        self.geometry("600x400")
        self.url = tk.Entry(self)
        self.url.pack(fill="x")
        self.url.bind("<Return>", self._load)
        self.text = st.ScrolledText(self)
        self.text.pack(fill="both", expand=True)

    def _load(self, _ev):
        h = self.url.get().strip()
        if not h.startswith("nb://"): return
        h = h[5:]
        threading.Thread(target=lambda: asyncio.run(self._fetch(h)), daemon=True).start()

    async def _fetch(self, h: str):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.node_port)
        writer.write(pack({"op": "get", "hash": h}))
        await writer.drain()
        resp = await unpack(reader)
        writer.close()
        await writer.wait_closed()
        raw = bytes.fromhex(resp["data"])
        meta = parse(raw.decode())
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"Title: {meta['title']}\n\n")
        self.text.insert(tk.END, meta["text"] + "\n")
        for url, label in meta["link"]:
            self.text.insert(tk.END, f"→ {label}  ({url})\n")

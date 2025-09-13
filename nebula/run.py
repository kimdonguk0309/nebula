import argparse, asyncio, os, signal, sys
from nebula.node import Node
from nebula.browser import Browser

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--bootstrap", help="IP:PORT of first node")
    parser.add_argument("--no-gui", action="store_true")
    args = parser.parse_args()

    os.makedirs("apps", exist_ok=True)
    node = Node(args.port, args.bootstrap)
    asyncio.create_task(node.start())

    if not args.no_gui:
        import tkinter as tk
        browser = Browser(args.port)
        browser.mainloop()
    else:
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

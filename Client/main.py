from src.core.client import *
from src.threads.apithread import ApiReqThread
#import websockets
#import asyncio

import sys
def main() -> int:
    ApiReqThread.init()
    client = Client(1080,540)
    client.run()
    return 0

#async def listen():
#    client_id = 1
#    url = f"ws://localhost:8000/ws/{client_id}"
#    async with websockets.connect(url) as ws:
#        while True:
#            await ws.send("Hello")
#            msg = await ws.recv()
#            print(msg)

#asyncio.get_event_loop().run_until_complete(listen())

if __name__ == '__main__':
    sys.exit(main())
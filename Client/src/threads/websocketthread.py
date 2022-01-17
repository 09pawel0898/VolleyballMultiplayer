import asyncio
import threading
import time
import queue
from queue import Queue
from src.networking.serverAPI.serverapi import *
from src.networking.serverRoom.packages import *
import websockets

class WebsocketThread:
    _thread : threading.Thread
    _bRunning = False
    _webSocket = None
    _remote = ""
    _roomHash = ""

    _pendingQueue = Queue()
    _responseQueue = Queue()

    @staticmethod
    async def _sending_handler():
       while WebsocketThread._bRunning:
            await asyncio.sleep(0.01)
            if not WebsocketThread._pendingQueue.empty():
                package_to_send : PackageSend = WebsocketThread._pendingQueue.get(block=True)
                await WebsocketThread._webSocket.send(package_to_send.json())
                if package_to_send.header == CodeSend.Disconnected:
                    await WebsocketThread._webSocket.close()
                    return

    @staticmethod
    async def _receiving_handler():
        while WebsocketThread._bRunning:
            try:
                package_received = await WebsocketThread._webSocket.recv()
                WebsocketThread._responseQueue.put(package_received)
            except:
                return

    @staticmethod
    async def _init_connection():
        url = WebsocketThread._remote + WebsocketThread._roomHash

        WebsocketThread._webSocket = await websockets.connect(url)

        WebsocketThread.send(
            PackageSend(
                header = CodeSend.Connected,
                body = ""
            )
        )
        await asyncio.gather(WebsocketThread._sending_handler(),
                             WebsocketThread._receiving_handler())
        WebsocketThread._bRunning = False

    @staticmethod
    def _run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(WebsocketThread._init_connection())
        loop.close()

    @staticmethod
    def send(package : PackageSend) -> None:
        WebsocketThread._pendingQueue.put(package)

    @staticmethod
    def try_receive() -> str | None:
        try:
            response = WebsocketThread._responseQueue.get(block=False)
        except queue.Empty:
            response = None
        return response

    @staticmethod
    def connect(room_hash: str) -> None:
        WebsocketThread._remote = "ws" + REMOTE[4:] + "/"
        WebsocketThread._roomHash = room_hash
        WebsocketThread._bRunning = True
        WebsocketThread._thread = threading.Thread(target=WebsocketThread._run,
                                                   args=())
        WebsocketThread._thread.start()

    @staticmethod
    def disconnect():
        WebsocketThread.send(
            PackageSend(
                header = CodeSend.Disconnected,
                body = "Disconnected"
            )
        )


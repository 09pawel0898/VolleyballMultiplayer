import asyncio
import threading
import json
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
                data = await WebsocketThread._webSocket.recv()
                package_received : PackageReceived = parse_recv_data(data)
                WebsocketThread._responseQueue.put(package_received)
            except:
                return

    @staticmethod
    async def _init_connection():
        url = WebsocketThread._remote + WebsocketThread._roomHash

        try:
            WebsocketThread._webSocket = await websockets.connect(url)
        except:
            WebsocketThread._responseQueue.put(PackageReceived(header=CodeReceived.Disconnect,
                                                               body=""))
            return

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
    def try_receive() -> PackageReceived | None:
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


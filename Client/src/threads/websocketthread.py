import asyncio
import queue
import threading
import time
from queue import Queue
from src.networking.serverAPI.serverapi import *
import websockets

class WebsocketThread:
    _thread : threading.Thread
    _bRunning = False

    _remote = ""
    _roomHash = ""

    # RoomRequest queue
    _pendingQueue = Queue()

    # RoomResponse queue
    _responseQueue = Queue()


    @staticmethod
    async def main_loop():
        url = WebsocketThread._remote + WebsocketThread._roomHash
        print(url)
        global_websocket = await websockets.connect(url)
        while WebsocketThread._bRunning:
            await asyncio.sleep(1)
            #await global_websocket.send("Hello")
            msg = await global_websocket.recv()
            print(msg)
            #pending = ApiReqThread._pendingQueue.get(block=True)
            #ApiReqThread._handle_request(pending)
            #time.sleep(0.1)
        global_websocket.close()

    @staticmethod
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(WebsocketThread.main_loop())
        loop.close()

    @staticmethod
    async def _handle_request(request: ApiRequest) -> None:
        pass
        # response = None
        # match request.type:
        #     case PendingRequest.GET_Temp:
        #         #response = ServerAPI.temp()
        #         pass
        #     case PendingRequest.POST_RegisterUser:
        #         response = ServerAPI.try_register_user(
        #             NewUser(username=request.data[0],password=request.data[1],email=request.data[2]))
        #
        #     case PendingRequest.POST_SigninUser:
        #         response = ServerAPI.try_authenticate_user(
        #             AuthUser(username=request.data[0],password=request.data[1]))
        #
        # if response is not None:
        #     ApiReqThread._responseQueue.put(ApiResponse(request, response))

    @staticmethod
    async def send(data) -> None:
        pass
        #WebsocketThread._pendingQueue.put(request)

    @staticmethod
    def try_receive() -> None:
        pass
        # try:
        #     response = ApiReqThread._responseQueue.get(block=False)
        # except queue.Empty:
        #     response = None
        # return response

    @staticmethod
    def connect(room_hash: str) -> None:
        WebsocketThread._remote = "ws" + REMOTE[4:] + "/"
        WebsocketThread._roomHash = room_hash

        WebsocketThread._bRunning = True
        WebsocketThread._thread = threading.Thread(target=WebsocketThread.run,
                                                   args=())
        WebsocketThread._thread.start()

    @staticmethod
    def disconnect():
        WebsocketThread._bRunning = False


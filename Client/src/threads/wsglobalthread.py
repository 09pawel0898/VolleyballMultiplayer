import asyncio
import queue
import threading
import time
from queue import Queue
from src.networking.serverAPI.serverapi import *
import websockets

class WSGlobalThread:
    _thread : threading.Thread
    _bRunning = False

    # GlobalRequest queue
    _pendingQueue = Queue()

    # GlobalResponse queue
    _responseQueue = Queue()


    @staticmethod
    async def main_loop():
        client_id = 1
        url = "ws://localhost:8000/ws/" + client_id.__str__()
        global_websocket = await websockets.connect(url)
        while WSGlobalThread._bRunning:
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
        loop.run_until_complete(WSGlobalThread.main_loop())
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
    async def new_request(request: ApiRequest) -> None:
        pass
        #ApiReqThread._pendingQueue.put(request)

    @staticmethod
    def try_get_response() -> ApiResponse:
        pass
        # try:
        #     response = ApiReqThread._responseQueue.get(block=False)
        # except queue.Empty:
        #     response = None
        # return response

    @staticmethod
    def init() -> None:
        WSGlobalThread._bRunning = True
        WSGlobalThread._thread = threading.Thread(target=WSGlobalThread.run,
                                                  args=())
        WSGlobalThread._thread.start()



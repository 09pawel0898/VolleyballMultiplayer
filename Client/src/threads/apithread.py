import queue
import threading
import time
from queue import Queue
from src.networking.serverAPI.serverapi import *

class ApiReqThread:
    _thread : threading.Thread
    _bRunning = False

    # ApiRequest queue
    _pendingQueue = Queue()

    # ApiResponse queue
    _responseQueue = Queue()

    @staticmethod
    def run():
        while ApiReqThread._bRunning:
            pending = ApiReqThread._pendingQueue.get(block=True)
            ApiReqThread._handle_request(pending)
            time.sleep(0.1)

    @staticmethod
    def _handle_request(request: ApiRequest) -> None:
        response = None
        match request.type:
            case PendingRequest.GET_Temp:
                #response = ServerAPI.temp()
                pass
            case PendingRequest.POST_RegisterUser:
                response = ServerAPI.try_register_user(
                    NewUser(username=request.data[0],password=request.data[1],email=request.data[2]))

            case PendingRequest.POST_SigninUser:
                response = ServerAPI.try_authenticate_user(
                    AuthUser(username=request.data[0],password=request.data[1]))

        if response is not None:
            ApiReqThread._responseQueue.put(ApiResponse(request, response))

    @staticmethod
    def new_request(request: ApiRequest) -> None:
        ApiReqThread._pendingQueue.put(request)

    @staticmethod
    def try_get_response() -> ApiResponse:
        try:
            response = ApiReqThread._responseQueue.get(block=False)
        except queue.Empty:
            response = None
        return response

    @staticmethod
    def init() -> None:
        ApiReqThread._bRunning = True
        ApiReqThread._thread = threading.Thread(target=ApiReqThread.run,
                                               args=())
        ApiReqThread._thread.start()



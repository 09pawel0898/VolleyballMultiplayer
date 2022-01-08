import queue
import threading
import time
from enum import Enum
from queue import Queue
from src.networking.serverAPI.serverapi import ServerAPI,User
from typing import Optional

class PendingRequest(Enum):
    GET_Temp = 1
    POST_RegisterUser = 2

class ApiRequest:
    def __init__(self, type : PendingRequest, data : Optional = None):
        self.type = type
        self.data = data

class ApiReqThread:
    _thread : threading.Thread
    _bRunning = False
    _pendingQueue = Queue()
    _responseQueue = Queue()

    @staticmethod
    def run():
        while ApiReqThread._bRunning:
            pending = ApiReqThread._pendingQueue.get(block=True)
            ApiReqThread._handle_request(pending)
            time.sleep(0.1)

    @staticmethod
    def _handle_request(request: ApiRequest):
        response = None
        match request.type:
            case PendingRequest.GET_Temp:
                response = ServerAPI.temp()
            case PendingRequest.POST_RegisterUser:
                response = ServerAPI.try_register_user(User(username=request.data[0],
                                                            password=request.data[1]))
        if response is not None:
            ApiReqThread._responseQueue.put(response)

    @staticmethod
    def new_request(request: ApiRequest):
        ApiReqThread._pendingQueue.put(request)

    @staticmethod
    def try_get_response():
        try:
            response = ApiReqThread._responseQueue.get(block=False)
        except queue.Empty:
            response = None
        return response

    @staticmethod
    def init():
        ApiReqThread._bRunning = True
        ApiReqThread._thread = threading.Thread(target=ApiReqThread.run,
                                               args=())
        ApiReqThread._thread.start()



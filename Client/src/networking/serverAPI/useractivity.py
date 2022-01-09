from abc import ABC,abstractmethod
from src.networking.serverAPI.serverapi import ApiResponse
from typing import Optional

class UserActivity:
    def __init__(self):
        pass

    @abstractmethod
    def handle_response(self, state, response : Optional[ApiResponse] = None):
        if response is not None:
            print(response)
import asyncio

import requests
from pydantic import BaseModel
from enum import Enum

REMOTE = "http://localhost:8000"

class User(BaseModel):
    username: str
    password: str

class ResponseStatus(Enum):
    Test = 1
    Ok = 2
    SignedUp = 3
    UsernameTaken = 4



class ServerAPI:
    decoder = {
        200: ResponseStatus.Ok,
        201: ResponseStatus.SignedUp,
        226: ResponseStatus.UsernameTaken
    }

    @staticmethod
    def temp() -> ResponseStatus:
        response = requests.get(REMOTE + "/temp/")
        return ServerAPI._decode(response.status_code)

    @staticmethod
    def try_register_user(user: User) -> ResponseStatus:
        response = requests.post(REMOTE+"/user-new/",data = user.json())
        return ServerAPI._decode(response.status_code)

    @staticmethod
    def _decode(status_code: int) -> ResponseStatus:
        return ServerAPI.decoder[status_code]


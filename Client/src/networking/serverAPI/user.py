import asyncio

import requests
from pydantic import BaseModel
from enum import Enum

REMOTE = "http://localhost:8000"

class User(BaseModel):
    username: str
    password: str

class SignUpStatus(Enum):
    SignedUp = 1
    UsernameTaken = 2

class ServerAPI:
    @staticmethod
    async def try_register_user(user: User):
        #await asyncio.sleep(1)
        response = requests.post(REMOTE+"/user-new/",data = user.json())
        print(response.status_code)
        #if response.status_code == 201:
        #    return SignUpStatus.SignedUp
        #elif response.status_code == 226:
        #    return SignUpStatus.UsernameTaken

from typing import Optional
from pydantic import BaseModel

class CreateRoom(BaseModel):
    host_username: str

class EnterRoom(BaseModel):
    rival_username: str
    hash: str

class DeleteRoom(BaseModel):
    host_username: str
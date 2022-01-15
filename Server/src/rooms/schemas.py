from typing import Optional
from pydantic import BaseModel

class CreateRoom(BaseModel):
    host_username: str

class EnterRoom(BaseModel):
    rival_username: str
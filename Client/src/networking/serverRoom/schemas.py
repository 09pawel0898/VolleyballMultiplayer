from pydantic import BaseModel
from ..serverAPI.schemas import Token

class RoomCreate(BaseModel):
    host_username: str

class NewRoom(BaseModel):
    token : Token
    room : RoomCreate
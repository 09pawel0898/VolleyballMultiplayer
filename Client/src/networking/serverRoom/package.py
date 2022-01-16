from pydantic import BaseModel
from enum import Enum

class Code(Enum):
    Null = 0
    Connect = 1
    Disconnect = 2

class DataType(Enum):
    BallBounce = 1

class StatusFrame(BaseModel):
    hash: str
    status: str

class DataFrame(BaseModel):
    header : DataType
    body: str

class Package(BaseModel):
    code : Code
    body : DataFrame | StatusFrame

from pydantic import BaseModel
from enum import Enum

class CodeSend(Enum):
    Null = 0
    Connected = 1
    Disconnected = 2
    StartClicked = 3

class CodeReceived(Enum):
    Null = 0
    Disconnect = 1
    BallBounced = 2
    StartTheGame = 3
    PlayerWon = 4
    PlayerLost = 5

class PackageSend(BaseModel):
    header : CodeSend
    body : str

class PackageReceived(BaseModel):
    header: CodeReceived
    body: str

# class DataType(Enum):
#     BallBounce = 1
#
# class StatusBo(BaseModel):
#     hash: str
#     status: str
#
# class DataFrame(BaseModel):
#     header : DataType
#     body: str
#

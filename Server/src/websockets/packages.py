from pydantic import BaseModel
from enum import Enum
import json

class CodeReceived(Enum):
    Null = 0
    Connected = 1
    Disconnected = 2
    StartClicked = 3

class CodeSend(Enum):
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

def parse_recv_data(data) -> PackageReceived:
    data_json = json.loads(data)
    return PackageReceived(header = data_json["header"],
                           body = data_json["body"])

def parse_package(package: PackageSend | PackageReceived) -> tuple[CodeSend|CodeReceived,str]:
    return package.header,package.body
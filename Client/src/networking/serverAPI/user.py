from src.core.states.stateidentifiers import StateID
from src.networking.serverAPI.useractivity import UserActivity
from enum import Enum

class UserLobbyActivity(Enum):
    Idle = 1

class BaseUser:
    def __init__(self) -> None:
        self.state : StateID
        self.activity : UserActivity

class Guest(BaseUser):
    def __init__(self) -> None:
        super().__init__()

class SignedUsed(BaseUser):
    def __init__(self, guest : Guest,username : str, token : str) -> None:
        super().__init__()
        self.username = username
        self.token = token
        self.state = guest.state
        self.activity = guest.activity

class User:
    me = Guest()



from src.core.states.stateidentifiers import StateID
from src.networking.serverAPI.useractivity import UserActivity
from enum import Enum

class UserLobbyActivity(Enum):
    Idle = 1

# this class handles user data
class User:
    def __init__(self):
        self.state : StateID
        self.activity : UserActivity

class SignedUsed(User):
    def __init__(self, username):
        super(SignedUsed, self).__init__()
        self.username = username
        #self.token = ..

class Guest(User):
    def __init__(self):
        super(Guest, self).__init__()

user = Guest()


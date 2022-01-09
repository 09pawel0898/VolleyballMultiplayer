from src.core.states.stateidentifiers import StateID
from enum import Enum

class UserMenuActivity(Enum):
    Idle = 1
    InLoginPanel = 2
    InRegisterPanel = 3
    WaitingForSignUpResponse = 4
    WaitingForSignInResponse = 5

class UserLobbyActivity(Enum):
    Idle = 1

# this class handles user data
class User:
    def __init__(self):
        self.state = StateID.MainMenu
        self.current_activity = UserMenuActivity.Idle

class SignedUsed(User):
    def __init__(self, username):
        super(SignedUsed, self).__init__()
        self.username = username
        #self.token = ..

class Guest(User):
    def __init__(self):
        super(Guest, self).__init__()
        # self.token = ..

user = Guest()
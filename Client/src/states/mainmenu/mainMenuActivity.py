from src.networking.serverAPI.useractivity import *
from src.networking.serverAPI.user import user
from src.networking.serverAPI.serverapi import ResponseStatus
from src.core.defines import DEBUG

from enum import Enum

class MainMenuActivityState(Enum):
    Idle = 1
    WaitingForSignUpResponse = 2
    WaitingForSignInResponse = 3
    
class MainMenuActivity(UserActivity):
    def __init__(self):
        super(MainMenuActivity, self).__init__()
        self._user = user
        self._activity_state = MainMenuActivityState.Idle

    def handle_response(self, state, response : Optional[ApiResponse] = None) -> bool:
        if response is not None:
            if DEBUG:
                print(response)
            if self._activity_state == MainMenuActivityState.WaitingForSignUpResponse:
                if response.response.status == ResponseStatus.SignedUp:
                    state.show_msg_box("User successfully registered.")
                    self._activity_state = MainMenuActivityState.Idle
                    return True
                elif response.response.status == ResponseStatus.UsernameTaken:
                    state.show_msg_box("This username is already taken.")
                    self._activity_state = MainMenuActivityState.Idle
                    return True
            if self._activity_state == MainMenuActivityState.WaitingForSignInResponse:
                if response.response.status == ResponseStatus.SignedIn:
                    state.show_msg_box("Logged in.")
                    self._activity_state = MainMenuActivityState.Idle
                    return True
                elif response.response.status == ResponseStatus.BadAuth:
                    state.show_msg_box("Bad username or password.")
                    self._activity_state = MainMenuActivityState.Idle
                    return True

            if response.response.status == ResponseStatus.ConnectionError:
                state.show_msg_box("Connection error.")
            elif response.response.status == ResponseStatus.TimeoutError:
                state.show_msg_box("Timeout.")
            return True
        else:
            return False

    def set_state(self, new_state: MainMenuActivityState):
        self._activity_state = new_state

    def get_state(self):
        return self._activity_state
from src.networking.serverAPI.useractivity import *
from src.networking.serverAPI.serverapi import ResponseStatus
from src.core.defines import DEBUG
from enum import Enum

class GameplayActivityState(Enum):
    Playing = 1

class GameplayActivity(UserActivity):
    def __init__(self):
        super(GameplayActivity, self).__init__()
        self._activity_state = GameplayActivityState.Playing

    def handle_response(self, state, response) -> bool:
        if response is not None:
            if DEBUG:
                print(response)
            # if self._activity_state == MainMenuActivityState.WaitingForSignUpResponse:
            #     if response.response.status == ResponseStatus.SignedUp:
            #         state.show_msg_box("User successfully registered.")
            #         self._activity_state = MainMenuActivityState.Idle
            #         return True
            if response.response.status == ResponseStatus.ConnectionError:
                state.show_msg_box("Connection error.")
            elif response.response.status == ResponseStatus.TimeoutError:
                state.show_msg_box("Timeout.")
            return True
        else:
            return False

    def set_state(self, new_state: GameplayActivityState):
        self._activity_state = new_state

    def get_state(self):
        return self._activity_state
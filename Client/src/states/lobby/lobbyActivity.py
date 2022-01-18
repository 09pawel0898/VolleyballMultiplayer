from src.networking.serverAPI.useractivity import *
from src.networking.serverAPI.serverapi import ResponseStatus,PendingRequest
from src.core.defines import DEBUG
from src.core.resources.resourceidentifiers import TextureID
from src.threads.websocketthread import WebsocketThread

from enum import Enum

class LobbyActivityState(Enum):
    Idle = 1
    RoomCreated = 2
    WaitingInRoom = 3
    WaitingForConnection = 4

class LobbyActivity(UserActivity):
    def __init__(self):
        super(LobbyActivity, self).__init__()
        self._activity_state = LobbyActivityState.Idle

    def handle_response(self, state, response) -> bool:
        if response is not None:
            if DEBUG:
                print(response)
            if response.request.type == PendingRequest.GET_AllRooms:
                if response.response.status == ResponseStatus.Ok:
                    state.room_label_manager.refresh()
            if response.request.type == PendingRequest.POST_CreateRoom:
                if response.response.status == ResponseStatus.Ok:
                    self._activity_state = LobbyActivityState.WaitingInRoom
                    room_hash = response.response.data["hash"]
                    WebsocketThread.connect(room_hash)
                    state.show_msg_box("Room created. Waiting..",TextureID.ButtonCancel, state._room_shutdown)
                else:
                    state.show_msg_box("Your room already exist.",TextureID.ButtonOk, state._hide_msg_box)
            if response.response.status == ResponseStatus.ConnectionError:
                state.show_msg_box("Connection error.")
            elif response.response.status == ResponseStatus.TimeoutError:
                state.show_msg_box("Timeout.")
            return True
        else:
            return False

    def set_state(self, new_state: LobbyActivityState):
        self._activity_state = new_state

    def get_state(self):
        return self._activity_state
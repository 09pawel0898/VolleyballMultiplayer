from src.networking.serverAPI.useractivity import *
from src.networking.serverAPI.serverapi import ResponseStatus
from src.core.defines import DEBUG
from src.core.resources.sprite import Sprite
from src.networking.serverRoom.packages import *
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
            header, body = parse_package(response)
            match header:
                case CodeReceived.BallMoved:
                    ball : Sprite = state.ball
                    new_positions = body.split(',')
                    ball.set_position(int(new_positions[0]),int(new_positions[1]))

    def set_state(self, new_state: GameplayActivityState):
        self._activity_state = new_state

    def get_state(self):
        return self._activity_state
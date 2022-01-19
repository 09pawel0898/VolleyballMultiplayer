from src.networking.serverAPI.useractivity import *
from src.core.util.logger import *
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

            header, body = parse_package(response)
            if DEBUG:
                Log.add(LogType.LogRoom,f"Received : [{header}][{body}]")

            match header:
                case CodeReceived.BallMoved:
                    ball : Sprite = state.ball
                    new_positions = body.split(',')
                    ball.set_position(int(new_positions[0]),int(new_positions[1]))
                case CodeReceived.StartTheGame:
                    pass
                    #set usernames
                case CodeReceived.InitNewRound:
                    state.hide_msg_box()
                    state.init_round(int(body))
                case CodeReceived.PlayerMoved:
                    new_positions = body.split(',')
                    state.gameplay_controller.rival_pawn.set_position(
                        float(new_positions[0]),float(new_positions[1]))
            return True

    def set_state(self, new_state: GameplayActivityState):
        self._activity_state = new_state

    def get_state(self):
        return self._activity_state
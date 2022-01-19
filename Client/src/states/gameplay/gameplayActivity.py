from src.networking.serverAPI.useractivity import *
from src.core.util.logger import *
from src.core.defines import DEBUG
from src.core.resources.sprite import Sprite
from src.core.resources.resourceidentifiers import TextureID
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
                case CodeReceived.InitBall:
                    state.init_ball(int(body))
                case CodeReceived.BallBounced:
                    params = body.split(',')
                    state.ball.set_position(float(params[0]),float(params[1]))
                    state.ball.speed = float(params[2])
                    state.ball.D = float(params[3])
                case CodeReceived.RoundEnd:
                    status = int(body)
                    state.update_score(status)
                    if status == 0:
                        #game lost
                        state.bReadyClicked = False
                        state.show_msg_box("You lost!Press OK to play again.",
                                           TextureID.ButtonOk,
                                           state._startgame_onclick)
                    elif status == 1:
                        #game won
                        state.show_msg_box("You won!Press OK to play again.",
                                           TextureID.ButtonOk,
                                           state._startgame_onclick)

            return True

    def set_state(self, new_state: GameplayActivityState):
        self._activity_state = new_state

    def get_state(self):
        return self._activity_state
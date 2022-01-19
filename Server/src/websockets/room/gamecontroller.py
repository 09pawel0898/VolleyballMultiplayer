from ..room.player import Player
from ..connection.packages import *
from src.defines import DEBUG
from src.logger import *

class GameController:
    def __init__(self, room_manager):
        self.bGameStarted = False
        self.bHostLeftSide = False
        self.bBallLeftSide = False
        self.host : Player|None = None
        self.rival : Player|None = None
        self.roomconnectionmanager = room_manager

    # async def send_start_the_game(self):
    #     if DEBUG:
    #         Log.add(LogType.LogRoom, f"Send : [broadcast][{CodeSend.StartTheGame}][]")
    #     await self.roomconnectionmanager.broadcast(
    #         PackageSend(
    #             header=CodeSend.StartTheGame,
    #             body=""))

    async def send_start_the_game_with_usernames(self):
        if DEBUG:
            Log.add(
                LogType.LogRoom,
                f"Send : [{self.host.websocket.client}][{CodeSend.StartTheGame}][{self.rival.username}]")
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.StartTheGame, body=self.rival.username), self.host.websocket)
        if DEBUG:
            Log.add(
                LogType.LogRoom,
                f"Send : [{self.rival.websocket.client}][{CodeSend.StartTheGame}][{self.host.username}]")
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.StartTheGame, body=self.host.username), self.rival.websocket)

    async def send_init_round(self):
        #0 - leftSide , 1 - rightSide
        host_side = "0"
        rival_side = "1"
        if DEBUG:
            Log.add(
                LogType.LogRoom,
                f"Send : [{self.host.websocket.client}][{CodeSend.InitNewRound}][{host_side}]")
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.InitNewRound, body=host_side), self.host.websocket)
        if DEBUG:
            Log.add(
                LogType.LogRoom,
                f"Send : [{self.rival.websocket.client}][{CodeSend.InitNewRound}][{rival_side}]")
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.InitNewRound, body=rival_side), self.rival.websocket)

    async def send_ball_bounced(self, websocket, body):
        if DEBUG:
            Log.add(
                LogType.LogRoom,
                f"Send : [{websocket.client}][{CodeSend.BallBounced}][{body}]")
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.BallBounced, body=body),
            websocket)

    async def send_init_ball(self):
        # 0 - leftSide , 1 - rightSide
        if self.bBallLeftSide:
            self.bBallLeftSide = False
            side = "1"
        else:
            self.bBallLeftSide = True
            side = "0"
        if DEBUG:
            Log.add(
                LogType.LogRoom,
                f"Send : [broadcast][{CodeSend.InitBall}][{side}]")
        await self.roomconnectionmanager.broadcast(
            PackageSend(header=CodeSend.InitBall, body=side))
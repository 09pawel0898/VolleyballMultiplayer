from ..room.player import Player
from ..connection.packages import *

class GameController:
    def __init__(self, room_manager):
        self.bGameStarted = False
        self.bHostLeftSide = False
        self.host : Player|None = None
        self.rival : Player|None = None
        self.roomconnectionmanager = room_manager

    async def send_start_the_game(self):
        await self.roomconnectionmanager.broadcast(
            PackageSend(
                header=CodeSend.StartTheGame,
                body=""))

    async def send_usernames_to_each_other(self):
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.StartTheGame, body=self.rival.username), self.host.websocket)
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.StartTheGame, body=self.host.username), self.rival.websocket)

    async def send_init_round(self):
        #0 - leftSide , 1 - rightSide
        if self.bHostLeftSide:
            self.bHostLeftSide = False
            host_side = "1"
            rival_side = "0"
        else:
            self.bHostLeftSide = True
            host_side = "0"
            rival_side = "1"
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.InitNewRound, body=host_side), self.host.websocket)
        await self.roomconnectionmanager.send_personal_message(
            PackageSend(header=CodeSend.InitNewRound, body=rival_side), self.rival.websocket)
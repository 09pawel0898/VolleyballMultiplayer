from typing import List
from fastapi import WebSocket
from ..room.gamecontroller import GameController
from .packages import *
from src.logger import *
from ..room.player import Player
from src.defines import DEBUG

class RoomConnectionManager:
    def __init__(self,room_hash: str):
        self.hash = room_hash
        self.active_connections: List[WebSocket] = []
        self.game_controller = GameController(self)
        self.people = 0
        self.host : Player|None = None
        self.rival : Player|None = None
        self.start_clicks = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def handle_recv_package(self,websocket: WebSocket, package: PackageReceived):
        header, body = parse_package(package)

        remote = websocket.client.__str__()
        if DEBUG:
            Log.add(LogType.LogRoom,f"Received : [{remote}][{header}][{body}]")
        match header:
            case CodeReceived.Connected:
                self.people += 1
                if self.people == 1:
                    self.game_controller.host = self.host = Player(websocket,body)
                elif self.people == 2:
                    self.game_controller.rival = self.rival = Player(websocket,body)
                    await self.game_controller.send_start_the_game_with_usernames()
            case CodeReceived.Disconnected:
                pass
            case CodeReceived.StartClicked:
                self.start_clicks+=1
                if self.start_clicks == 2:
                    self.game_controller.bGameStarted = True
                    await self.game_controller.send_init_round()
                    await self.game_controller.send_init_ball()
            # case CodeReceived.BallMoved:
            #     await self.broadcast(PackageSend(header=CodeSend.BallMoved, body=body))
            case CodeReceived.BallBounced:
                if self._received_from_host(websocket):
                    await self.game_controller.send_ball_bounced(self.rival.websocket, body)
                elif self._received_from_rival(websocket):
                    await self.game_controller.send_ball_bounced(self.host.websocket, body)

            case CodeReceived.PlayerMoved:
                if self._received_from_host(websocket):
                    await self.send_personal_message(
                        PackageSend(header=CodeSend.PlayerMoved, body=body),
                        self.rival.websocket)
                elif self._received_from_rival(websocket):
                    await self.send_personal_message(
                        PackageSend(header=CodeSend.PlayerMoved, body=body),
                        self.host.websocket)

            case CodeReceived.BallTouchedFloor:
                if self.game_controller.bGameStarted == True:
                    side = int(body)
                    winner = self.host
                    self.start_clicks = 0
                    if self.game_controller.bHostLeftSide:
                        if side == 0:
                            winner: Player = self.host
                        elif side == 1:
                            winner: Player = self.rival
                    else:
                        if side == 0:
                            winner: Player = self.rival
                        elif side == 1:
                            winner: Player = self.host
                    loser : Player = self.host if winner == self.rival else self.rival
                    await self.send_personal_message(
                        PackageSend(header=CodeSend.RoundEnd, body="0"),
                        loser.websocket)
                    await self.send_personal_message(
                        PackageSend(header=CodeSend.RoundEnd, body="1"),
                        winner.websocket)
                self.game_controller.bGameStarted = False

    def _received_from_host(self, websocket) ->bool:
        if websocket == self.host.websocket:
            return True
        else:
            return False

    def _received_from_rival(self, websocket) ->bool:
        if websocket == self.rival.websocket:
            return True
        else:
            return False

    async def send_personal_message(self, package: PackageSend, websocket: WebSocket):
        await websocket.send_text(package.json())

    async def broadcast(self, package: PackageSend):
        for connection in self.active_connections:
            await connection.send_text(package.json())
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
            # case CodeReceived.BallMoved:
            #     await self.broadcast(PackageSend(header=CodeSend.BallMoved, body=body))
            case CodeReceived.PlayerMoved:
                if websocket == self.host.websocket:
                    await self.send_personal_message(
                        PackageSend(header=CodeSend.PlayerMoved, body=body),
                        self.rival.websocket)
                elif websocket == self.rival.websocket:
                    await self.send_personal_message(
                        PackageSend(header=CodeSend.PlayerMoved, body=body),
                        self.host.websocket)


    async def send_personal_message(self, package: PackageSend, websocket: WebSocket):
        await websocket.send_text(package.json())

    async def broadcast(self, package: PackageSend):
        for connection in self.active_connections:
            await connection.send_text(package.json())
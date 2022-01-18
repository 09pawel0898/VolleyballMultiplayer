from typing import List
from fastapi import WebSocket
from ..room.gamecontroller import GameController
from .packages import *

class RoomConnectionManager:
    def __init__(self,room_hash: str):
        self.hash = room_hash
        self.active_connections: List[WebSocket] = []
        self.game_controller = GameController()
        self.people = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def handle_recv_package(self,package: PackageReceived):
        header, body = parse_package(package)

        match header:
            case CodeReceived.Connected:
                self.people += 1
                if self.people == 2:
                    if not self.game_controller.bGameStarted:
                        await self.broadcast(PackageSend(
                            header=CodeSend.StartTheGame,
                            body=""))
            case CodeReceived.Disconnected:
                pass

    async def send_personal_message(self, package: PackageSend, websocket: WebSocket):
        await websocket.send_text(package.json())

    async def broadcast(self, package: PackageSend):
        for connection in self.active_connections:
            await connection.send_text(package.json())
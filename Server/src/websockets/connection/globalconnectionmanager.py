from typing import List
from fastapi import WebSocket
from .roomconnectionmanager import RoomConnectionManager
from .packages import *

class GlobalConnectionManager:
    def __init__(self):
        self.room_manager: dict[str, RoomConnectionManager] = {}

    async def connect_to_room(self, room_hash :str, websocket: WebSocket):
        if not room_hash in self.room_manager:
            self.room_manager[room_hash] = RoomConnectionManager(room_hash)
        await self.room_manager[room_hash].connect(websocket)

    def disconnect_from_room(self, room_hash: str, websocket: WebSocket):
        self.room_manager[room_hash].active_connections.remove(websocket)
        self._delete_room(room_hash)

    def get_room(self, room_hash: str):
        return self.room_manager[room_hash]

    def _delete_room(self, room_hash: str):
        self.room_manager.pop(room_hash)

    async def send_personal_message(self, room_hash: str, package: PackageSend, websocket: WebSocket):
        await self.room_manager[room_hash].send_personal_message(package, websocket)

    async def broadcast(self, room_hash: str, package: PackageSend):
        await self.room_manager[room_hash].broadcast(package)
from typing import List

class RoomDisplayed:
    def __init__(self, host: str, hash: str, players: int):
        self.host_username = host
        self.hash = hash
        self.players = players

class RoomHolder:
    rooms : List[RoomDisplayed] = []

    @staticmethod
    def add_room(room: RoomDisplayed):
        RoomHolder.rooms.append(room)

    @staticmethod
    def clear():
        RoomHolder.rooms.clear()


class RoomCreate:
    def __init__(self, host: str):
        pass

    def create(self):
        pass

class RoomJoin:
    def __init__(self):
        pass

    def join(self):
        pass
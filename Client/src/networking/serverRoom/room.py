

class Room:
    def __init__(self, host: str):
        self.host_username = host
        self.people = 0

class RoomCreate(Room):
    def __init__(self, host: str):
        super().__init__(host)
        pass

    def create(self):
        pass

class RoomJoin(Room):
    def __init__(self):
        pass

    def join(self):
        pass
from fastapi import WebSocket

class Player:
    def __init__(self,websocket: WebSocket, username:str):
        self.host = websocket.client.host
        self.port = websocket.client.port
        self.websocket = websocket
        self.username = username
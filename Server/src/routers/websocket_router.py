from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect, status
import json
from ..websockets.globalconnectionmanager import GlobalConnectionManager
from sqlalchemy.orm import Session
from src.database import get_db
from ..rooms import models,crud
from ..websockets.packages import *

router = APIRouter(
    tags=["Websocket"]
)

global_connection_manager = GlobalConnectionManager()

@router.websocket("/{room_hash}")
async def room_endpoint(websocket: WebSocket, room_hash: str, db: Session = Depends(get_db)):
    existing_room = crud.is_room_existing(db,room_hash)
    if not existing_room:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    elif existing_room.players >= 2:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    await global_connection_manager.connect_to_room(room_hash,websocket)

    crud.set_players_in_room(db,room_hash,existing_room.players + 1)

    try:
        #await global_connection_manager.send_personal_message(room_hash, "Ga", websocket)
        while True:
            data = await websocket.receive_text()
            if data is not None:
                header, body = parse_package(parse_recv_data(data))
                if header == CodeReceived.Connected:
                    global_connection_manager.get_room(room_hash).people+=1
                    if global_connection_manager.get_room(room_hash).people == 2:
                        await global_connection_manager.broadcast(room_hash, "GameStarted")


            await global_connection_manager.send_personal_message(room_hash, "Ga", websocket)
            #await global_connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        global_connection_manager.disconnect_from_room(room_hash, websocket)
        global_connection_manager.delete_room(room_hash)
        result = crud.delete_room_by_hash(db=db, room_hash = room_hash)
        if result:
            print(f"Room {room_hash} deleted because one of players has left.")
        #await global_connection_manager.broadcast("Client left the game.")
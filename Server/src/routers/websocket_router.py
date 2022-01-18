from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect, status
from src.websockets.connection.globalconnectionmanager import GlobalConnectionManager
from sqlalchemy.orm import Session
from src.database import get_db
from ..rooms import crud
from src.websockets.connection.packages import *
from src.logger import *

router = APIRouter(
    tags=["Websocket"]
)

global_connection_manager = GlobalConnectionManager()

@router.websocket("/{room_hash}")
async def room_endpoint(websocket: WebSocket, room_hash: str, db: Session = Depends(get_db)):
    #check if room exists in database or if it is not full
    existing_room = crud.is_room_existing(db,room_hash)
    if not existing_room:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    elif existing_room.players >= 2:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    #connect player, increase room players in database
    await global_connection_manager.connect_to_room(room_hash,websocket)
    crud.set_players_in_room(db,room_hash,existing_room.players + 1)

    #proceed until one of players disconnect
    try:
        while True:
            recv_data = await websocket.receive_text()
            if recv_data is not None:
                package = parse_recv_data(recv_data)
                await global_connection_manager.get_room(room_hash).handle_recv_package(package)
    except WebSocketDisconnect:
        global_connection_manager.disconnect_from_room(room_hash, websocket)
        if crud.delete_room_by_hash(db=db, room_hash = room_hash):
            Log.add(LogType.LogWS,f"Room {room_hash} deleted because one of players has left.")

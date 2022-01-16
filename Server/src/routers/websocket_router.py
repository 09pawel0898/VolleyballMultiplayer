from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect, status
from sqlalchemy import update

from ..websockets.globalwebsocketmanager import GlobalConnectionManager
from sqlalchemy.orm import Session
from src.database import get_db
from ..rooms import models,crud

router = APIRouter(
    tags=["Websocket"]
)

global_connection_manager = GlobalConnectionManager()

@router.websocket("/{room_hash}")
async def global_endpoint(websocket: WebSocket, room_hash: str, db: Session = Depends(get_db)):
    await global_connection_manager.connect(websocket)

    existing_room = db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first()
    if not existing_room:
        global_connection_manager.disconnect(websocket)

    if existing_room.players > 2:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    stmt = (update(models.Rooms).
            where(models.Rooms.hash == room_hash).
            values(players=existing_room.players + 1)
            )
    db.execute(stmt)
    db.commit()

    try:
        while True:
            data = await websocket.receive_text()
            if data is not None:
                print(data)
            await global_connection_manager.send_personal_message("Hello user", websocket)
            #await global_connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        global_connection_manager.disconnect(websocket)
        result = crud._delete_room_by_hash(db=db, hash = room_hash)
        if result:
            print(f"Room {room_hash} deleted due to being empty.")
        #await global_connection_manager.broadcast("Client left the game.")
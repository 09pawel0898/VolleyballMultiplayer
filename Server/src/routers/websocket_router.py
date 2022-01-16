from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect, status
from sqlalchemy import update

from ..websockets.globalconnectionmanager import GlobalConnectionManager
from sqlalchemy.orm import Session
from src.database import get_db
from ..rooms import models,crud

router = APIRouter(
    tags=["Websocket"]
)

global_connection_manager = GlobalConnectionManager()

@router.websocket("/{room_hash}")
async def room_endpoint(websocket: WebSocket, room_hash: str, db: Session = Depends(get_db)):
    await global_connection_manager.connect_to_room(room_hash,websocket)

    existing_room = db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first()
    if not existing_room:
        global_connection_manager.disconnect_from_room(room_hash,websocket)

    if existing_room.players >= 2:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    stmt = (update(models.Rooms).
            where(models.Rooms.hash == room_hash).
            values(players=existing_room.players + 1)
            )
    db.execute(stmt)
    db.commit()

    print(db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first().players)

    try:
        #await global_connection_manager.send_personal_message(room_hash, "Ga", websocket)
        while True:
            data = await websocket.receive_text()
            if data is not None:
                print(data)
            await global_connection_manager.send_personal_message(room_hash, "Ga", websocket)
            #await global_connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        global_connection_manager.disconnect_from_room(room_hash, websocket)
        global_connection_manager.delete_room(room_hash)
        result = crud.delete_room_by_hash(db=db, room_hash = room_hash)
        if result:
            print(f"Room {room_hash} deleted because one of players has left.")
        #await global_connection_manager.broadcast("Client left the game.")
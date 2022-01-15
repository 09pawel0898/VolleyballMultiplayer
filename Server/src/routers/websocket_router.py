from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect, status
from ..websockets.globalwebsocketmanager import GlobalConnectionManager
from sqlalchemy.orm import Session
from src.database import get_db
from ..rooms import models

router = APIRouter(
    tags=["Websocket"]
)

global_connection_manager = GlobalConnectionManager()

@router.websocket("/ws/{room_hash}")
async def global_endpoint(websocket: WebSocket, room_hash: str, db: Session = Depends(get_db)):
    players_in_room =  db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first().players
    if players_in_room > 2:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first().update(
        {"players" : players_in_room + 1}
    )
    db.commit()
    print(players_in_room + 1)

    await global_connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data is not None:
                print(data)
            await global_connection_manager.send_personal_message("Hello user", websocket)
            #await global_connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        global_connection_manager.disconnect(websocket)
        await global_connection_manager.broadcast("Client left the game.")
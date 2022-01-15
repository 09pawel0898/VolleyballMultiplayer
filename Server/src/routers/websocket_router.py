from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from ..websockets.globalwebsocketmanager import GlobalConnectionManager

router = APIRouter(
    tags=["Websocket"]
)

global_connection_manager = GlobalConnectionManager()

@router.websocket("/ws/{client_id}")
async def global_endpoint(websocket: WebSocket, client_id: int):
    await global_connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await global_connection_manager.send_personal_message(f"You wrote: {data}", websocket)
            await global_connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        global_connection_manager.disconnect(websocket)
        await global_connection_manager.broadcast(f"Client #{client_id} left the chat")
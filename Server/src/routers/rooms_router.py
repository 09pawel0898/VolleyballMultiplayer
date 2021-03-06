from fastapi import Depends, APIRouter, Response, status
from sqlalchemy.orm import Session
from ..users.schemas import Token
from ..users.crud import get_current_user
from src.database import get_db
from ..rooms import crud,schemas, models
from ..exceptions.httpexceptions import credentials_exception

router = APIRouter(
    tags=["Rooms"]
)

@router.post("/rooms/create/")
async def create_room(token: Token, room: schemas.CreateRoom, response: Response, db: Session = Depends(get_db)):
    user = get_current_user(token=token.access_token,db=db)
    if not user:
        raise credentials_exception
    result = crud.create_room(db=db, room=room)
    if result:
        return result
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"data" : f"Error when creating a room"}

@router.delete("/rooms/delete/")
async def delete_room(token: Token, room: schemas.DeleteRoom, response: Response, db: Session = Depends(get_db)):
    user = get_current_user(token=token.access_token,db=db)
    if not user:
        raise credentials_exception
    result = crud.delete_room(db=db, room=room)
    if result:
        return {"data" : f"{room.host_username}'s room succesfully deleted"}
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"data" : f"Cant destroy this room"}

#temporary
@router.delete("/rooms/delete-all")
async def delete_all(db: Session = Depends(get_db)):
    try:
        db.query(models.Rooms).delete()
        db.commit()
        return {"data": "All room succesfully deleted"}
    except:
        db.rollback()
        return {"data" : "Error uccured when deleting the rooms"}


@router.get("/rooms/all/")
async def get_all_rooms(db: Session = Depends(get_db)):
    return db.query(models.Rooms).all()

#
# @router.post("/auth/register", status_code=status.HTTP_201_CREATED)
# async def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
#     result = crud.create_user(db=db, user=user)
#     if result:
#         return result
#     else:
#         response.status_code = status.HTTP_226_IM_USED
#         return {"data" : f"username {user.username} is already in use"}

#@router.get("/room/delete/")
#async def delete_room(db: Session = Depends(get_db), current_user: models.Users = Depends(crud.get_current_user)):
#    pass

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..users import models
from src.database import get_db
from ..users import crud

router = APIRouter(
    tags=["Rooms"]
)

@router.post("/room/create/")
async def create_room(db: Session = Depends(get_db), current_user: models.Users = Depends(crud.get_current_user)):
    pass

@router.get("/room/delete")
async def delete_room(db: Session = Depends(get_db), current_user: models.Users = Depends(crud.get_current_user)):
    pass

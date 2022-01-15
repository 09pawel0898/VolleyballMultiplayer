from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..users.schemas import Token
from ..users import models
from src.database import get_db
from ..users import crud

router = APIRouter(
    tags=["Users"]
)

@router.get("/users/me/")
async def get_user_me(token: Token, db: Session = Depends(get_db)):
    return crud.get_current_user(token=token.access_token,db=db)

@router.get("/users/all/")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

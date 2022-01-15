from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..users import models
from src.database import get_db
from ..users import crud

router = APIRouter(
    tags=["Users"]
)

@router.get("/user/me/")
async def read_users_me(current_user: models.Users = Depends(crud.get_current_user)):
    return current_user

@router.get("/all/")
async def get_all(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

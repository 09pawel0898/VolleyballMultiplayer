from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ..users import models
from src.database import get_db
from ..users import crud

router = APIRouter(
    tags=["Users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/user/me/")
def read_users_me(current_user: models.Users = Depends(crud.get_current_user)):
    return current_user

@router.get("/all/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

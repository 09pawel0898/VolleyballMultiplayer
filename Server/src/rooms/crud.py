import random
import string

from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from src.rooms import schemas,models
from src.database import get_db
from jose import JWTError, jwt
from .schemas import CreateRoom,EnterRoom
from ..exceptions.httpexceptions import host_already_has_room_exception

def generate_new_room_hash() -> str:
    pool = string.ascii_letters + string.digits
    return ''.join(random.choices(pool, k=20))

def create_room(db: Session, room: schemas.CreateRoom):
    hash = generate_new_room_hash()
    db_room = models.Rooms(host=room.host_username,
                           players=0,
                           hash=hash)
    try:
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
    except:
        raise host_already_has_room_exception
    return db_room
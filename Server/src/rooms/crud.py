import random
import string
from sqlalchemy.orm import Session
from src.rooms import schemas,models
from ..exceptions.httpexceptions import host_already_has_room_exception, no_such_room_exception
from sqlalchemy import update

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

def is_room_existing(db: Session, room_hash: str):
    existing = db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first()
    if existing:
        return existing
    else:
        return None

def set_players_in_room(db: Session, room_hash: str, new_players: int):
    stmt = (update(models.Rooms).
            where(models.Rooms.hash == room_hash).
            values(players=new_players)
            )
    db.execute(stmt)
    db.commit()

def delete_room(db: Session, room: schemas.DeleteRoom):
    try:
        room = db.query(models.Rooms).filter(models.Rooms.host == room.host_username).first()
        db.delete(room)
        db.commit()
    except:
        raise no_such_room_exception
    return room

def delete_room_by_hash(db: Session, room_hash: str):
    try:
        room = db.query(models.Rooms).filter(models.Rooms.hash == room_hash).first()
        db.delete(room)
        db.commit()
    except:
        raise no_such_room_exception
    return room

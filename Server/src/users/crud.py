from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from src.users import schemas
from src.users import models
from src.database import get_db
from jose import JWTError, jwt

SECRET_KEY= "85b7b65fff27cbf1f4e2b8574a20ffe5d7fccf1d9a4348b5fc58f7671650d243"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db,username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(username=user.username,
                           hashed_password=get_password_hash(user.password),
                           email=user.email)
    existing_user = db.query(models.Users).filter(models.Users.username == user.username).first()
    if not existing_user:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
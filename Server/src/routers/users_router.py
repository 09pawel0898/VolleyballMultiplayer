from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import models, crud, schemas
from src.database import get_db
from jose import JWTError, jwt

router = APIRouter(
    tags=["Users"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/")
def read_users_me(current_user: models.Users = Depends(get_current_user)):
    return current_user

@router.post("/user-new/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
    result = crud.create_user(db=db, user=user)
    if result:
        return result
    else:
        response.status_code = status.HTTP_226_IM_USED
        return {"data" : f"username {user.username} is already in use"}

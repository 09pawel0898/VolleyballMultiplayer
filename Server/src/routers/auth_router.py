from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from src.users import crud, schemas
from src.database import get_db

router = APIRouter(
    tags=["Authentication"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
    result = crud.create_user(db=db, user=user)
    if result:
        return result
    else:
        response.status_code = status.HTTP_226_IM_USED
        return {"data" : f"username {user.username} is already in use"}

@router.post("/auth/login", response_model=schemas.Token, status_code=status.HTTP_202_ACCEPTED)
def login_for_access_token(auth_user: schemas.UserAuth, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, auth_user.username, auth_user.password)
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
from fastapi import FastAPI
from src.database import engine
from .routers import users_router, auth_router
from .users import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router.router)
app.include_router(auth_router.router)



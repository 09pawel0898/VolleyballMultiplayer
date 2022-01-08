from fastapi import FastAPI
from src.database import engine
from .routers import users_router, models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users_router.router)

@app.get("/temp/")
def temp():
    return {"temp":"temp"}


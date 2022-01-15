from sqlalchemy import Column, Integer, String
from src.database import Base

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    host = Column(String, unique=True)
    players = Column(Integer)
    hash = Column(String)

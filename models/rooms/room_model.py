from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from base.db import Base


class Rooms(Base):
    __tablename__ = "room_f"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    capacity = Column(String(5))

    # room_movie_scheduler = relationship("Scheduling", back_populates="room_scheduler")

    pass


class RoomCreate(BaseModel):
    name: str
    capacity: str


class RoomUpdate(BaseModel):
    name: str
    capacity: str


class Room(RoomCreate):
    id: int

    class Config:
        orm_mode = True

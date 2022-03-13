from typing import Optional, List

from pydantic import BaseModel
from pydantic.schema import date
from sqlalchemy import Column, Integer, String, DATE

from base.db import Base
from models.rooms.room_model import Room
from models.schedule.schedule_model import Time


class Movies(Base):
    __tablename__ = "movies_f"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    photoURL = Column(String(255))
    rating = Column(String(255))
    duration = Column(String(255))
    genre = Column(String(255))
    availFrom = Column(DATE, default=date.today())
    availTo = Column(DATE, default=date.today())
    active = Column(Integer, default=1)

    pass


class MovieCreate(BaseModel):
    name: str
    description: str
    photoURL: str
    rating: str
    duration: str
    genre: str
    availFrom: date
    availTo: date


class MovieUpdate(BaseModel):
    name: str
    description: str
    photoURL: str
    rating: str
    duration: str
    genre: str
    availFrom = date
    availTo = date


class MovieSchedule(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    rating: str
    duration: str
    genre: str
    photoURL: str
    rooms: List[Room]
    times: List[Time]


class Movie(MovieCreate):
    id: int

    class Config:
        orm_mode = True

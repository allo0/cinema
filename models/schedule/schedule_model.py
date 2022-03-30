from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey

from base.db import Base


class Scheduling(Base):
    __tablename__ = "room_movie_schedule2"

    id = Column(Integer, primary_key=True, index=True)

    movie = Column(String(255),ForeignKey('movies_f.name', ondelete='CASCADE'), nullable=False)
    room = Column(String(255), ForeignKey('room_f.name', ondelete='CASCADE'), nullable=False)
    date = Column(String(255))
    time = Column(String(255))

    active = Column(Integer, default=1)

    pass


class ScheduleCreateUpdate(BaseModel):
    room: str
    date: str
    time: str


class SchedulingCreate(BaseModel):
    movie: str
    details: List[ScheduleCreateUpdate]


class SchedulingResponse(BaseModel):
    id: int
    movie: str
    room: str
    date: str
    time: str


class Schedule(SchedulingCreate):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


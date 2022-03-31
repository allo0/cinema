from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey

from base.db import Base


class Scheduling(Base):
    __tablename__ = "room_movie_schedule_f_2"

    id = Column(Integer, primary_key=True, index=True)

    movie = Column(String(255), ForeignKey('movies_f.name', ondelete='CASCADE'), nullable=False)
    room = Column(String(255), ForeignKey('room_f.name', ondelete='CASCADE'), nullable=False)
    date = Column(String(255))
    time = Column(String(255))
    maxSeats = Column(String(5))
    remSeats = Column(String(5))

    active = Column(Integer, default=1)

    pass


class ScheduleCreate(BaseModel):
    room: str
    date: str
    time: str
    maxSeats: Optional[str] = None
    remSeats: Optional[str] = None


class ScheduleUpdate(BaseModel):
    room: str
    date: str
    time: str

    remSeats: str


class SchedulingUpdate(BaseModel):
    movie: str
    details: List[ScheduleUpdate]


class SchedulingCreate(BaseModel):
    movie: str
    details: List[ScheduleCreate]


class SchedulingResponse(BaseModel):
    id: int
    movie: str
    room: str
    date: str
    time: str
    maxSeats: str
    remSeats: str


class Schedule(SchedulingCreate):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

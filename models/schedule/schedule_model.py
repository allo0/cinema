from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, DATE, TIME

from base.db import Base


class Scheduling(Base):
    __tablename__ = "room_movie_schedule_f"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, index=True)
    room_id = Column(Integer)
    viewingDate = Column(DATE)
    viewingTime = Column(TIME)
    active = Column(Integer,default=1)

    pass


class Time(BaseModel):
    room_id: int
    date: str
    time: str


class Details(BaseModel):
    room: str
    date: str
    time: str


class SchedulingCreate(BaseModel):
    movie: str
    details: List[Details]

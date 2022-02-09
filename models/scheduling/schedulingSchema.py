from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Details(BaseModel):
    room: str
    date: str
    time: str


class SchedulingCreate(BaseModel):
    movie: str
    details: List[Details]


####

class Room(BaseModel):
    room_id: int
    name: str
    capacity: str


class Time(BaseModel):
    room_id: int
    date: str
    time: str


class Movie(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    rating: str
    duration: str
    genre: str
    photoURL: str
    rooms: List[Room]
    times: List[Time]


class CalendarDetails(BaseModel):
    movies: List[Movie]


class CalendarModel(BaseModel):
    calendar_details: CalendarDetails

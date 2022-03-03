from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import TIMESTAMP


class MoviesBase(BaseModel):
    name: str


class MovieCreate(MoviesBase):
    description: Optional[str] = None
    photoURL: Optional[str] = None
    rating: Optional[str] = None
    duration: Optional[str] = None
    genre: Optional[str] = None
    availFrom: Optional[date] = None
    availTo: Optional[date] = None
    active: Optional[int] = None


class Movies(MoviesBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

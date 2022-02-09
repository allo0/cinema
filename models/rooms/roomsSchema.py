from typing import List, Optional
from pydantic import BaseModel, Field


class RoomsBase(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None


# class MovieCreate(RoomsBase):
#     desrciption: Optional[str] = None
#     rating: Optional[str] = None
#     duration: Optional[str] = None
#     genre: Optional[str] = None


class Rooms(RoomsBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

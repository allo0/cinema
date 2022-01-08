from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    photoUrl: Optional[str] = None

class UserCreate(UserBase):
    password: str




class UserLogin(BaseModel):
    username: Optional[str] = None
    password: str
    email: Optional[str] = None


class User(UserBase):
    id: int
    is_active: Optional[str] = None

    class Config:
        orm_mode = True

from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    photoUrl: Optional[str] = None


class UserCreate(UserBase):
    id: Optional[str] = None
    password: Optional[str] = None




class UserLogin(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    id: Optional[str] = None


class User(UserBase):
    user_id: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True

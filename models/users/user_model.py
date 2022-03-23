from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mysql import LONGTEXT

from base.db import Base


class UserModel(Base):
    __tablename__ = "users_f"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    user_id = Column(String(255), index=True)
    username = Column(String(255), index=True)
    password = Column(String(255))
    firstName = Column(String(255))
    lastName = Column(String(255))
    photoUrl = Column(LONGTEXT)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    user_type = Column(Integer, default=0)
    activation_code = Column(String(255))
    __table_args__ = (UniqueConstraint('email', 'user_id', 'username', name='uc_email_id_username'),)

    pass


class UserCreate(BaseModel):
    email: str
    username: Optional[str] = None
    user_id: Optional[str] = None
    password: Optional[str] = None
    firstName: str
    lastName: str
    photoUrl: Optional[str] = None
    user_type: Optional[int] = None
    activation_code: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    photoUrl: Optional[str] = None
    user_type: Optional[int] = None



class User(UserCreate):
    id: int

    class Config:
        orm_mode = True

from pydantic import Field

from base.db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Enum
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    photoUrl = Column(String)
    createdAt = Column(TIMESTAMP)
    is_active = Column(Boolean, default=False)

    user_type = relationship("UserType", back_populates="owner")

    pass


class userType_Enum(Integer, Enum):
    user = 1
    ticketer = 2
    admin = 4


class UserType(Base):
    __tablename__ = "userType"

    id = Column(Integer, primary_key=True, index=True)
    userType = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    owner = relationship("User", back_populates="user_type")

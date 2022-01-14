from base.db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
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

from pydantic import Field

from base.db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Enum
from sqlalchemy.orm import relationship


class Rooms(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    capacity = Column(String)

    # room_movie_scheduler = relationship("Scheduling", back_populates="room_scheduler")

    pass


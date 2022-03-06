from DateTime import DateTime
from pydantic import Field

from base.db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Enum, DATE
from sqlalchemy.orm import relationship


class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    photoURL = Column(String)
    rating = Column(String)
    duration = Column(String)
    genre = Column(String)
    availFrom = Column(DATE)
    availTo = Column(DATE)
    active = Column(Integer)


    # room_movie_scheduler = relationship("Scheduling", back_populates="movie_scheduler")

    pass

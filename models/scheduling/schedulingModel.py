from sqlalchemy import Column, Integer, DATE, TIME

from base.db import Base


class Scheduling(Base):
    __tablename__ = "room_movie_schedule"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, index=True)
    room_id = Column(Integer)
    viewingDate = Column(DATE)
    viewingTime = Column(TIME)

    pass

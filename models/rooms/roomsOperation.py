from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.rooms import roomsSchema


def get_room(db: Session, name: Optional[str] = None, id: Optional[str] = None):
    from models.rooms import roomsModel
    room = db.query(roomsModel.Rooms)
    if name is not None:
        room = room.filter(roomsModel.Rooms.name == name)
    if id is not None:
        room = room.filter(roomsModel.Rooms.id == id)
    room = room.first()
    return room


def add_room(db: Session, room_: roomsSchema.Rooms):
    from models.rooms import roomsModel
    db_room = roomsModel.Rooms(name=room_.name, capacity=room_.capacity)

    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    return db_room

from typing import Optional

from sqlalchemy.orm import Session


def get_room(db: Session, name: Optional[str] = None, id: Optional[str] = None):
    from models.rooms import room_model
    room = db.query(room_model.Rooms)
    if name is not None:
        room = room.filter(room_model.Rooms.name == name)
    if id is not None:
        room = room.filter(room_model.Rooms.id == id)
    room = room.first()
    return room

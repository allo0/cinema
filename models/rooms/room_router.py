from fastapi_crudrouter import SQLAlchemyCRUDRouter

from base.db import Base, engine, get_db
from models.rooms.room_model import Room, RoomCreate, RoomUpdate, Rooms

Base.metadata.create_all(bind=engine)
roomRouter = SQLAlchemyCRUDRouter(
    schema=Room,
    create_schema=RoomCreate,
    update_schema=RoomUpdate,
    db_model=Rooms,
    db=get_db,
    prefix='rooms',
    delete_all_route=False,
    tags=['Rooms']

)

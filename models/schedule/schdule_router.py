from fastapi import Depends, HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlmodel import Session
from starlette import status

from base.db import Base, engine, get_db
from models.schedule import schedule_controller
from models.schedule.schedule_model import SchedulingCreate, Schedule, Scheduling

Base.metadata.create_all(bind=engine)
scheduleRouter = SQLAlchemyCRUDRouter(
    schema=Schedule,
    create_schema=SchedulingCreate,

    db_model=Scheduling,
    db=get_db,
    prefix='schedule',
    create_route=False,
    get_one_route=False,
    get_all_route=False,
    delete_all_route=False,
    update_route=False,
    delete_one_route=False,
    tags=['Schedule']

)


@scheduleRouter.post('')
def add_to_schedule(srm: SchedulingCreate, db: Session = Depends(get_db)):
    added_to_schedule = schedule_controller.add_to_schedule(db=db, movie=srm.movie, details=srm.details)

    if added_to_schedule == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Room or Movie not found",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    if added_to_schedule == 200:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Added to schedule",
                            headers={"WWW-Authenticate": "Bearer"},
                            )


@scheduleRouter.get("")
def get_schedule(parameters: str, availFrom: str, availTo: str, db: Session = Depends(get_db)):
    if parameters == "calendar" and availFrom is not None and availTo is not None:
        from models.schedule.schedule_controller import get_from_schedule
        movies = get_from_schedule(db=db, availFrom=availFrom, availTo=availTo)
        return {"status": 200, "calendar_details": movies}
    else:
        return {"status": 400, "calendar_details": "Wrong Search Parameters"}


@scheduleRouter.get("/all")
def get_schedule_as_list(parameters: str, db: Session = Depends(get_db)):
    if parameters == "list":
        from models.schedule.schedule_controller import get_sch_list
        list = get_sch_list(db=db)
        print(list)
        return {"status": 200, "calendar_details": list}
    else:
        return {"status": 400, "calendar_details": "Wrong Search Parameters"}


@scheduleRouter.put("/{schedule_id}")
def update_to_schedule(schedule_id: int, srm: SchedulingCreate, db: Session = Depends(get_db)):
    from models.schedule.schedule_controller import update_schedule

    status = update_schedule(db=db, schedule_id=schedule_id, movie=srm.movie, room=srm.details[0].room,
                             date=srm.details[0].date,
                             time=srm.details[0].time)

    if status == 1:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Updated schedule",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    else:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail="Did not modify schedule",
                            headers={"WWW-Authenticate": "Bearer"},
                            )


@scheduleRouter.delete("/{schedule_id}")
def delete_from_schedule(schedule_id: int, db: Session = Depends(get_db)):
    from models.schedule.schedule_controller import delete_from_schedule

    status = delete_from_schedule(db=db, schedule_id=schedule_id)

    if status == 1:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Deleted from schedule",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    else:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail="Did not modify schedule",
                            headers={"WWW-Authenticate": "Bearer"},
                            )

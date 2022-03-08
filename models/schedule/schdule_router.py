from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from base.db import Base, engine, get_db
from models.schedule.schedule_model import SchedulingCreate

Base.metadata.create_all(bind=engine)
scheduleRouter = APIRouter(
    tags=["Schedule"],
    responses={404: {"description": "Not found"}},
)


@scheduleRouter.post('/schedule')
async def add_Movie_To_Schedule(srm: SchedulingCreate, db: Session = Depends(get_db)):
    from models.schedule import schedule_controller

    trans_completed = schedule_controller.add_to_schedule(db=db, movie=srm.movie, details=srm.details)
    if not trans_completed:
        return {"status": 400,
                "scheduling_info": "Schedule was unsuccessful"}
    return {"status": 200,
            "scheduling_info": "Schedule updated successfully"}


@scheduleRouter.get("/schedule")
async def get_schedule(parameters: str, db: Session = Depends(get_db), availFrom: str = None,
                       availTo: str = None):
    if parameters == "calendar" and availFrom is not None and availTo is not None:
        from models.schedule.schedule_controller import get_to_calendar
        movies = get_to_calendar(db=db, availFrom=availFrom, availTo=availTo)
        return {"status": 200, "calendar_details": movies}
    else:
        return {"status": 400, "calendar_details": "Wrong Search Parameters"}

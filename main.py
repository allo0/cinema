from fastapi import FastAPI, Depends, Request, Response
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from base.config import settings
from base.db import SessionLocal
from models.auth.token import get_current_active_user
from models.movies.movie_router import movieRouter
from models.open.open_router import openRouter
from models.rooms.room_router import roomRouter
from models.schedule.schdule_router import scheduleRouter
from models.users.user_router import userRouter

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)  # , root_path="http://127.0.0.1:5000"
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")


origins = [
    "https://cinema-front-end.herokuapp.com/",
    "https://cinema-thingy-1124.herokuapp.com/",
    "http://127.0.0.1:5000/",
    "http://localhost:4200/",
]



@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 24 hours
async def expire_movies(db: Session):
    from models.movies import movie_model
    movies = db.query(movie_model.Movies)
    movies = movies.filter(movie_model.Movies.active == 1)
    movies = movies.all()

    from datetime import datetime
    from models.schedule import schedule_model

    from models.schedule.schedule_controller import get_room_movie_time
    for movie in movies:
        if str(movie.availTo) < datetime.today().strftime('%Y-%m-%d'):
            moviex = db.query(movie_model.Movies)
            moviex = moviex.filter(movie_model.Movies.id == movie.id)
            moviex = moviex.filter(movie_model.Movies.active == 1)
            moviex = moviex.update({movie_model.Movies.active: 0})
            db.commit()
            for i in range(0, len(get_room_movie_time(db, movie.id))):
                sch = db.query(schedule_model.Scheduling) \
                    .filter(schedule_model.Scheduling.movie_id == movie.id) \
                    .update({schedule_model.Scheduling.active: 0})
                db.commit()

        else:
            continue


app.include_router(movieRouter, dependencies=[Depends(get_current_active_user)], prefix='/v1')
app.include_router(roomRouter, dependencies=[Depends(get_current_active_user)], prefix='/v1')
app.include_router(scheduleRouter, dependencies=[Depends(get_current_active_user)], prefix='/v1')
app.include_router(userRouter, dependencies=[Depends(get_current_active_user)], prefix='/v1')
app.include_router(openRouter, prefix='/v1')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#####

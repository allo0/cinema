from typing import Optional

from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from models.movies import moviesSchema


@repeat_every(seconds=60 * 60 * 24)  # 24 hours
def expire_movies(db: Session):
    from models.movies import moviesModel
    movies = db.query(moviesModel.Movies)
    movies = movies.filter(moviesModel.Movies.active == 1)
    movies = movies.all()

    from datetime import datetime
    from models.scheduling import schedulingModel
    import models.scheduling.srmOperation
    from models.scheduling.srmOperation import get_room_movie_time
    for movie in movies:
        if str(movie.availTo) < datetime.today().strftime('%Y-%m-%d'):
            moviex = db.query(moviesModel.Movies)
            moviex = moviex.filter(moviesModel.Movies.id == movie.id)
            moviex = moviex.filter(moviesModel.Movies.active == 1)
            moviex = moviex.update({moviesModel.Movies.active: 0})
            db.commit()
            for i in range(0, len(get_room_movie_time(db, movie.id))):
                sch = db.query(schedulingModel.Scheduling) \
                    .filter(schedulingModel.Scheduling.movie_id == movie.id) \
                    .update({schedulingModel.Scheduling.active: 0})
                db.commit()

        else:
            continue



def get_movie(db: Session, name: Optional[str] = None, id: Optional[str] = None):
    from models.movies import moviesModel
    movies = db.query(moviesModel.Movies)
    movies = movies.filter(moviesModel.Movies.active == 1)
    if name is not None:
        movies = movies.filter(moviesModel.Movies.name == name)
    if id is not None:
        movies = movies.filter(moviesModel.Movies.id == id)

    movies = movies.filter(moviesModel.Movies.active == 1)
    movies = movies.first()
    return movies


def get_movies(db: Session, name: Optional[str] = None, availFrom: Optional[str] = None,
               availTo: Optional[str] = None,
               genre: Optional[list] = None, ratingFrom: Optional[str] = None, ratingTo: Optional[str] = None,
               durationFrom: Optional[str] = None, durationTo: Optional[str] = None, skip: int = 0,
               limit: Optional[int] = None):
    from models.movies import moviesModel
    from sqlalchemy import and_
    movies = db.query(moviesModel.Movies)
    movies = movies.filter(moviesModel.Movies.active == 1)
    if name is not None:
        movies = movies.filter(moviesModel.Movies.name == name)

    if availFrom is not None and availTo is not None:
        movies = movies.filter(and_(
            moviesModel.Movies.availFrom >= availFrom,
            moviesModel.Movies.availTo <= availTo,
        ))
    elif availFrom is not None:
        movies = movies.filter(moviesModel.Movies.availFrom >= availFrom)
    elif availTo is not None:
        movies = movies.filter(moviesModel.Movies.availTo <= availTo)

    if genre is not None:
        movies = movies.filter(moviesModel.Movies.genre.in_(genre))

    if ratingTo is not None and ratingFrom is not None:
        movies = movies.filter(moviesModel.Movies.rating >= float(ratingFrom))
        movies = movies.filter(moviesModel.Movies.rating <= float(ratingTo))
    elif ratingFrom is not None:
        movies = movies.filter(moviesModel.Movies.rating >= float(ratingFrom))
    elif ratingTo is not None:
        movies = movies.filter(moviesModel.Movies.rating <= float(ratingTo))

    if durationFrom is not None and durationTo is not None:
        movies = movies.filter(moviesModel.Movies.duration >= float(durationFrom))
        movies = movies.filter(moviesModel.Movies.duration <= float(durationTo))
    elif durationFrom is not None:
        movies = movies.filter(moviesModel.Movies.duration >= float(durationFrom))
    elif durationTo is not None:
        movies = movies.filter(moviesModel.Movies.duration <= float(durationTo))

    movies = movies.offset(skip).limit(limit).all()

    return movies


def add_movie(db: Session, movie_: moviesSchema.MovieCreate):
    from models.movies import moviesModel
    db_movie = moviesModel.Movies(name=movie_.name, description=movie_.description, photoURL=movie_.photoURL,
                                  rating=movie_.rating, duration=movie_.duration, genre=movie_.genre,
                                  availFrom=movie_.availFrom, availTo=movie_.availTo, active=1)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

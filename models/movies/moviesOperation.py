from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.testing import in_

from models.movies import moviesSchema


def get_movie(db: Session, name: Optional[str] = None, id: Optional[str] = None):
    from models.movies import moviesModel
    movies = db.query(moviesModel.Movies)

    if name is not None:
        movies = movies.filter(moviesModel.Movies.name == name)
    if id is not None:
        movies = movies.filter(moviesModel.Movies.id == id)

    movies = movies.first()
    return movies


def get_movies(db: Session, name: Optional[str] = None, availFrom: Optional[str] = None, availTo: Optional[str] = None,
               genre: Optional[list] = None, ratingFrom: Optional[str] = None, ratingTo: Optional[str] = None,
               durationFrom: Optional[str] = None, durationTo: Optional[str] = None, skip: int = 0,
               limit: Optional[int] = None):
    from models.movies import moviesModel
    from sqlalchemy import and_
    movies = db.query(moviesModel.Movies)

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
                                  availFrom=movie_.availFrom, availTo=movie_.availTo)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

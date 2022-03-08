from typing import Optional

from sqlalchemy.orm import Session

from models.movies import movie_model


def get_movie(db: Session, name: Optional[str] = None, id: Optional[str] = None):
    from models.movies import movie_model
    movies = db.query(movie_model.Movies)
    movies = movies.filter(movie_model.Movies.active == 1)  # questionable reason for that

    if name is not None:
        movies = movies.filter(movie_model.Movies.name == name)
    if id is not None:
        movies = movies.filter(movie_model.Movies.id == id)

    movies = movies.filter(movie_model.Movies.active == 1)
    movies = movies.first()
    return movies


def get_movies(db: Session, name: Optional[str] = None, availFrom: Optional[str] = None, availTo: Optional[str] = None,
               genre: Optional[list] = None, ratingFrom: Optional[str] = None, ratingTo: Optional[str] = None,
               durationFrom: Optional[str] = None, durationTo: Optional[str] = None, skip: int = 0,
               limit: Optional[int] = None):
    from models.movies import movie_model
    from sqlalchemy import and_
    movies = db.query(movie_model.Movies)
    movies = movies.filter(movie_model.Movies.active == 1)
    if name is not None:
        movies = movies.filter(movie_model.Movies.name == name)

    if availFrom is not None and availTo is not None:
        movies = movies.filter(and_(
            movie_model.Movies.availFrom >= availFrom,
            movie_model.Movies.availTo <= availTo,
        ))
    elif availFrom is not None:
        movies = movies.filter(movie_model.Movies.availFrom >= availFrom)
    elif availTo is not None:
        movies = movies.filter(movie_model.Movies.availTo <= availTo)

    if genre is not None:
        movies = movies.filter(movie_model.Movies.genre.in_(genre))

    if ratingTo is not None and ratingFrom is not None:
        movies = movies.filter(movie_model.Movies.rating >= float(ratingFrom))
        movies = movies.filter(movie_model.Movies.rating <= float(ratingTo))
    elif ratingFrom is not None:
        movies = movies.filter(movie_model.Movies.rating >= float(ratingFrom))
    elif ratingTo is not None:
        movies = movies.filter(movie_model.Movies.rating <= float(ratingTo))

    if durationFrom is not None and durationTo is not None:
        movies = movies.filter(movie_model.Movies.duration >= float(durationFrom))
        movies = movies.filter(movie_model.Movies.duration <= float(durationTo))
    elif durationFrom is not None:
        movies = movies.filter(movie_model.Movies.duration >= float(durationFrom))
    elif durationTo is not None:
        movies = movies.filter(movie_model.Movies.duration <= float(durationTo))

    movies = movies.offset(skip).limit(limit).all()

    return movies


def add_movie(db: Session, movie_: movie_model.MovieCreate):
    from models.movies import movie_model
    db_movie = movie_model.Movies(name=movie_.name, description=movie_.description, photoURL=movie_.photoURL,
                                  rating=movie_.rating, duration=movie_.duration, genre=movie_.genre,
                                  availFrom=movie_.availFrom, availTo=movie_.availTo, active=1)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

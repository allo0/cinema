from typing import Optional

from fastapi import Depends, Query
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session

from base.db import Base, engine, get_db
from models.movies.movie_model import Movie, MovieCreate, MovieUpdate, Movies

Base.metadata.create_all(bind=engine)
movieRouter = SQLAlchemyCRUDRouter(
    schema=Movie,
    create_schema=MovieCreate,
    update_schema=MovieUpdate,
    db_model=Movies,
    db=get_db,
    prefix='movies',
    delete_all_route=False,
    tags=['Movies']

)


@movieRouter.get("/search/{parameters}")
async def search_movies(parameters: str, db: Session = Depends(get_db), name: Optional[str] = None,
                        availFrom: Optional[str] = None,
                        availTo: Optional[str] = None, genre: Optional[list[str]] = Query(None),
                        ratingFrom: Optional[str] = None, ratingTo: Optional[str] = None,
                        durationFrom: Optional[str] = None, durationTo: Optional[str] = None, skip: int = 0,
                        limit: Optional[int] = None):
    from models.movies.movie_controller import get_movies
    if parameters == "find":
        movies = get_movies(db=db, name=name, availFrom=availFrom, availTo=availTo, genre=genre, ratingTo=ratingTo,
                            ratingFrom=ratingFrom, durationFrom=durationFrom, durationTo=durationTo, skip=skip,
                            limit=limit)
        return {"status": 200, "details": {"movieCount": len(movies), "details": movies}}
    else:
        return {"status": 400, "details": "Wrong Search Parameters"}

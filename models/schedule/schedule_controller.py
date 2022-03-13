from typing import Optional

from sqlalchemy.orm import Session


def get_room_movie_time(db: Session, movie_id):
    from models.schedule import schedule_model
    return db.query(schedule_model.Scheduling) \
        .filter(
        schedule_model.Scheduling.movie_id == movie_id).all()


def get_date(db: Session, room_id: Optional[str] = None, movie_id: Optional[str] = None):
    from models.schedule import schedule_model

    dates = db.query(schedule_model.Scheduling)

    if movie_id is not None:
        dates = dates.filter(schedule_model.Scheduling.movie_id == movie_id)
    if room_id is not None:
        dates = dates.filter(schedule_model.Scheduling.room_id == room_id)
    dates = dates.first()

    return dates


def get_dates(db: Session, movie_id: Optional[str] = None, room_id: Optional[str] = None,
              availFrom: Optional[str] = None,
              availTo: Optional[str] = None):
    from models.schedule import schedule_model

    dates = db.query(schedule_model.Scheduling)

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        dates = dates.filter(and_(
            schedule_model.Scheduling.viewingDate >= availFrom,
            schedule_model.Scheduling.viewingDate <= availTo,
        ))
    elif availFrom is not None:
        dates = dates.filter(schedule_model.Scheduling.viewingDate >= availFrom)
    elif availTo is not None:
        dates = dates.filter(schedule_model.Scheduling.viewingDate <= availTo)
    if movie_id is not None:
        dates = dates.filter(schedule_model.Scheduling.movie_id == movie_id)
    if room_id is not None:
        dates = dates.filter(schedule_model.Scheduling.room_id == room_id)
    dates = dates.all()

    return dates


def count_movies(db: Session, availFrom: Optional[str] = None, availTo: Optional[str] = None):
    from models.schedule import schedule_model
    movies = db.query(schedule_model.Scheduling.movie_id).distinct()
    movies = movies.filter(schedule_model.Scheduling.active == 1)

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        movies = movies.filter(and_(
            schedule_model.Scheduling.viewingDate >= availFrom,
            schedule_model.Scheduling.viewingDate <= availTo,
        ))
    elif availFrom is not None:
        movies = movies.filter(schedule_model.Scheduling.viewingDate >= availFrom)
    elif availTo is not None:
        movies = movies.filter(schedule_model.Scheduling.viewingDate <= availTo)

    # movies = movies.group_by(schedulingModel.Scheduling.movie_id).all()
    movies = movies.all()

    return movies


def get_movies_in_dates(db: Session, availFrom: Optional[str] = None, availTo: Optional[str] = None):
    from models.schedule import schedule_model

    movies = db.query(schedule_model.Scheduling.movie_id).distinct()

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        movies = movies.filter(and_(
            schedule_model.Scheduling.viewingDate >= availFrom,
            schedule_model.Scheduling.viewingDate <= availTo,
        ))
    elif availFrom is not None:
        movies = movies.filter(schedule_model.Scheduling.viewingDate >= availFrom)
    elif availTo is not None:
        movies = movies.filter(schedule_model.Scheduling.viewingDate <= availTo)

    # movies = movies.group_by(schedulingModel.Scheduling.movie_id).all()
    movies = movies.all()

    return movies


def get_rooms_in_dates(db: Session, movie_id: Optional[str] = None, availFrom: Optional[str] = None,
                       availTo: Optional[str] = None):
    from models.schedule import schedule_model

    rooms = db.query(schedule_model.Scheduling.room_id).distinct()

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        rooms = rooms.filter(and_(
            schedule_model.Scheduling.viewingDate >= availFrom,
            schedule_model.Scheduling.viewingDate <= availTo,
        ))
    elif availFrom is not None:
        rooms = rooms.filter(schedule_model.Scheduling.viewingDate >= availFrom)
    elif availTo is not None:
        rooms = rooms.filter(schedule_model.Scheduling.viewingDate <= availTo)
    if movie_id is not None:
        rooms = rooms.filter(schedule_model.Scheduling.movie_id == movie_id)

    rooms = rooms.all()

    return rooms


def get_to_calendar(db: Session, availFrom: Optional[str] = None, availTo: Optional[str] = None):
    # Movies ID
    moviesID = count_movies(db=db, availFrom=availFrom, availTo=availTo)

    movies = []
    rooms = []
    times = []

    # Final object to return
    movie_to_calendar = []
    # Loop for each unique movie entry in the schedule timeframe we want
    for movie in range(0, len(count_movies(db=db, availFrom=availFrom, availTo=availTo))):
        print(moviesID[movie].movie_id)

        # -------------- Movies
        from models.movies.movie_controller import get_movie
        movies.append(get_movie(db=db, id=moviesID[movie].movie_id))

        # -------------- Rooms
        schedule_rooms = get_rooms_in_dates(db=db, movie_id=moviesID[movie].movie_id, availFrom=availFrom,
                                            availTo=availTo)
        from models.rooms.room_controller import get_room
        for room_ in schedule_rooms:
            rooms.append(get_room(db=db, id=room_.room_id))

        # -------------- Time & Date
        schedule_times = get_dates(db=db, movie_id=moviesID[movie].movie_id, availFrom=availFrom, availTo=availTo)

        for time in schedule_times:
            times.append(get_date(db=db, room_id=time.room_id))
        # return schedule_times
        # -------------- Room Schema
        from models.rooms.room_model import Rooms
        room_to_calendar = []
        for room in rooms:
            room_to_calendar.append(Rooms(id=room.id, name=room.name, capacity=room.capacity))

        # -------------- Time & Day Schema
        from models.schedule.schedule_model import Time
        time_to_calendar = []
        for time in times:
            time_to_calendar.append(Time(room_id=time.room_id, time=str(time.viewingTime), date=str(time.viewingDate)))

        # -------------- Movie Schema
        from models.movies.movie_model import MovieSchedule
        for movie in movies:
            movie_to_calendar.append(
                MovieSchedule(id=movie.id, name=movie.name, description=movie.description, rating=movie.rating,
                              duration=movie.duration, genre=movie.genre, photoURL=movie.photoURL,
                              rooms=room_to_calendar, times=time_to_calendar))

        movies = []
        rooms = []
        times = []
    return {"movies": movie_to_calendar}


def add_to_schedule(db: Session, movie: str, details: list):
    from models.movies import movie_controller
    from models.rooms import room_controller

    movie = movie_controller.get_movie(db=db, name=movie)

    if movie is None:
        return False

    for det in details:
        room_is = room_controller.get_room(db=db, name=det.room)

        if room_is is None:
            return False

    from models.schedule import schedule_model
    room_movie_time = []
    for det in details:
        room_id = room_controller.get_room(db=db, name=det.room)
        room_movie_time.append(schedule_model.Scheduling(movie_id=movie.id, room_id=room_id.id, viewingDate=det.date,
                                                         viewingTime=det.time, active=1))
    db.add_all(room_movie_time)
    db.commit()

    return True

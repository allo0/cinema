from typing import Optional

from sqlalchemy.orm import Session


def get_sch_list(db: Session, movie: Optional[str] = None, room: Optional[str] = None,
                 availFrom: Optional[str] = None,
                 availTo: Optional[str] = None):
    from models.schedule import schedule_model
    dates = db.query(schedule_model.Scheduling)
    dates = dates.filter(schedule_model.Scheduling.active == 1)

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        dates = dates.filter(and_(
            schedule_model.Scheduling.date >= availFrom,
            schedule_model.Scheduling.date <= availTo,
        ))
    elif availFrom is not None:
        dates = dates.filter(schedule_model.Scheduling.date >= availFrom)
    elif availTo is not None:
        dates = dates.filter(schedule_model.Scheduling.date <= availTo)
    if movie is not None:
        dates = dates.filter(schedule_model.Scheduling.movie == movie)
    if room is not None:
        dates = dates.filter(schedule_model.Scheduling.room == room)
    dates = dates.all()

    return dates


def update_schedule(db: Session, schedule_id: int, movie: Optional[str] = None, room: Optional[str] = None,
                    date: Optional[str] = None, time: Optional[str] = None, remSeats: Optional[str] = None):
    from models.schedule import schedule_model

    upd = db.query(schedule_model.Scheduling) \
        .filter(schedule_model.Scheduling.id == schedule_id) \
        .update({schedule_model.Scheduling.movie: movie, schedule_model.Scheduling.room: room,
                 schedule_model.Scheduling.date: date, schedule_model.Scheduling.time: time,
                 schedule_model.Scheduling.remSeats: remSeats})
    return upd


def delete_from_schedule(db: Session, schedule_id: int):
    from models.schedule import schedule_model

    upd = db.query(schedule_model.Scheduling) \
        .filter(schedule_model.Scheduling.id == schedule_id).delete()
    db.commit()
    return upd


def get_date(db: Session, room: Optional[str] = None, movie: Optional[str] = None):
    from models.schedule import schedule_model

    dates = db.query(schedule_model.Scheduling)

    if movie is not None:
        dates = dates.filter(schedule_model.Scheduling.movie == movie)
    if room is not None:
        dates = dates.filter(schedule_model.Scheduling.room == room)
    dates = dates.first()

    return dates


def get_dates(db: Session, movie: Optional[str] = None, room: Optional[str] = None,
              availFrom: Optional[str] = None,
              availTo: Optional[str] = None):
    from models.schedule import schedule_model

    dates = db.query(schedule_model.Scheduling)

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        dates = dates.filter(and_(
            schedule_model.Scheduling.date >= availFrom,
            schedule_model.Scheduling.date <= availTo,
        ))
    elif availFrom is not None:
        dates = dates.filter(schedule_model.Scheduling.date >= availFrom)
    elif availTo is not None:
        dates = dates.filter(schedule_model.Scheduling.date <= availTo)
    if movie is not None:
        dates = dates.filter(schedule_model.Scheduling.movie == movie)
    if room is not None:
        dates = dates.filter(schedule_model.Scheduling.room == room)
    dates = dates.all()

    return dates


def count_movies(db: Session, availFrom: Optional[str] = None, availTo: Optional[str] = None):
    from models.schedule import schedule_model
    movies = db.query(schedule_model.Scheduling.movie).distinct()
    movies = movies.filter(schedule_model.Scheduling.active == 1)

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        movies = movies.filter(and_(
            schedule_model.Scheduling.date >= availFrom,
            schedule_model.Scheduling.date <= availTo,
        ))
    elif availFrom is not None:
        movies = movies.filter(schedule_model.Scheduling.date >= availFrom)
    elif availTo is not None:
        movies = movies.filter(schedule_model.Scheduling.date <= availTo)

    # movies = movies.group_by(schedulingModel.Scheduling.movie_id).all()
    movies = movies.all()

    return movies


def get_rooms_in_dates(db: Session, movie: Optional[str] = None, availFrom: Optional[str] = None,
                       availTo: Optional[str] = None):
    from models.schedule import schedule_model

    rooms = db.query(schedule_model.Scheduling.room).distinct()

    if availFrom is not None and availTo is not None:
        from sqlalchemy import and_
        rooms = rooms.filter(and_(
            schedule_model.Scheduling.date >= availFrom,
            schedule_model.Scheduling.date <= availTo,
        ))
    elif availFrom is not None:
        rooms = rooms.filter(schedule_model.Scheduling.date >= availFrom)
    elif availTo is not None:
        rooms = rooms.filter(schedule_model.Scheduling.date <= availTo)
    if movie is not None:
        rooms = rooms.filter(schedule_model.Scheduling.movie == movie)

    rooms = rooms.all()

    return rooms


def get_from_schedule(db: Session, availFrom: Optional[str] = None, availTo: Optional[str] = None):
    # Movies ID
    moviesID = count_movies(db=db, availFrom=availFrom, availTo=availTo)

    movies = []
    rooms = []
    times = []

    # Final object to return
    movie_to_calendar = []
    # Loop for each unique movie entry in the schedule timeframe we want
    for movie in range(0, len(count_movies(db=db, availFrom=availFrom, availTo=availTo))):

        # -------------- Movies
        from models.movies.movie_controller import get_movie
        movies.append(get_movie(db=db, name=moviesID[movie][0]))

        # -------------- Rooms
        schedule_rooms = get_rooms_in_dates(db=db, movie=moviesID[movie][0], availFrom=availFrom,
                                            availTo=availTo)

        from models.rooms.room_controller import get_room
        for room_ in schedule_rooms:
            rooms.append(get_room(db=db, name=room_[0]))

        # -------------- Time & Date
        schedule_times = get_dates(db=db, movie=moviesID[movie][0], availFrom=availFrom, availTo=availTo)

        for time in schedule_times:
            times.append(get_date(db=db, room=time.room))
        # return schedule_times
        # -------------- Room Schema
        from models.rooms.room_model import Rooms
        room_to_calendar = []
        for room in rooms:
            room_to_calendar.append(Rooms(id=room.id, name=room.name, capacity=room.capacity))

        # -------------- Time & Day Schema
        from models.schedule.schedule_model import ScheduleCreate
        time_to_calendar = []
        for time in times:
            time_to_calendar.append(
                ScheduleCreate(room=time.room, time=str(time.time), date=str(time.date)))

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

    movie_exists = movie_controller.get_movie(db=db, name=movie)

    if movie_exists is None:
        return 404

    for det in details:
        room_is = room_controller.get_room(db=db, name=det.room)
        if room_is is None:
            return 404

    from models.schedule import schedule_model
    room_movie_time = []
    for det in details:
        room_movie_time.append(schedule_model.Scheduling(movie=movie, room=det.room, date=det.date,
                                                         time=det.time, maxSeats=det.maxSeats, remSeats=det.remSeats,
                                                         active=1))
    db.add_all(room_movie_time)
    db.commit()

    return 200

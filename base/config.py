import os

class Settings:
    PROJECT_NAME:str = "TicketReservationThingy"
    PROJECT_VERSION: str = "0.0.1"

MYSQLLPASS=os.environ.get("MYSQLPASS")
DBHOST=os.environ.get("DBHOST")
# ENV="Local"
ENV="Heroku"


settings = Settings()
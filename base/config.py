import os

class Settings:
    PROJECT_NAME:str = "TicketReservationThingy"
    PROJECT_VERSION: str = "0.0.1"

    REDIS_URL=os.environ.get("REDIS_URL")


settings = Settings()
from pathlib import Path

from fastapi_mail import ConnectionConfig
from starlette.templating import Jinja2Templates


class Settings:
    PROJECT_NAME: str = "TicketReservationThingy"
    PROJECT_VERSION: str = "0.1.1"


conf = ConnectionConfig(
    MAIL_FROM="protalpapei@gmail.com",
    MAIL_USERNAME="protalpapei@gmail.com",
    MAIL_PASSWORD="protalprotal",
    MAIL_FROM_NAME="CinemaThingy",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates/emails',
)
templates = Jinja2Templates(directory="templates")


# MYSQLLPASS = os.environ.get("MYSQLPASS")
# DBHOST = os.environ.get("DBHOST")


settings = Settings()

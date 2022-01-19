from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from base.config import MYSQLLPASS,DBHOST


SQLALCHEMY_DATABASE_URL = "mysql://root:"+MYSQLLPASS+"@"+DBHOST+"/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

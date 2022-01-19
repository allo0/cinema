from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from base.config import MYSQLLPASS,DBHOST


SQLALCHEMY_DATABASE_URL = "mysql://root:"+str(MYSQLLPASS)+"@"+str(DBHOST)+"/test"
# SQLALCHEMY_DATABASE_URL = "mysql://root:mao2mao2mao@mysoftendb.ccn9u77vnttp.us-east-2.rds.amazonaws.com/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

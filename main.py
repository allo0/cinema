from datetime import timedelta, datetime

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from base.db import SessionLocal
from base.config import settings
from models.token import TokenData
from models.user import userSchema, userOperation
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.user.userOperation import authenticate_user
from models.user.userSchema import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "3d781d186bbeaaec8405d529c23a18a7d9c53e3bf94b1c3ea259df93e42fbcfe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Connect with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = userOperation.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="User not authenticated")
    return current_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/v1/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/v1/register/", response_model=userSchema.User)
def create_user(user: userSchema.UserCreate, db: Session = Depends(get_db)):
    db_user = userOperation.check_if_user_exists(db, email=user.email, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return userOperation.create_user(db=db, user_=user)


@app.get("/v1/users/", response_model=List[userSchema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = userOperation.get_users(db, skip=skip, limit=limit)
    return users



@app.get("/v1/users/me/", response_model=userSchema.User)
async def read_users_me(current_user: userSchema.User = Depends(get_current_user)):
    return current_user

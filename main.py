from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

import models.token
from base.config import settings
from base.db import SessionLocal
from models.token import redis_conn
from models.user import userSchema, userOperation
from models.user.userSchema import UserLogin

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

origins = [
    "https://cinema-thingy-1124.herokuapp.com",
    "http://127.0.0.1:5000",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
tokenSettings = models.token.Settings()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# Connect with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/v1/register/", response_model=userSchema.User)
def create_user(user: userSchema.UserCreate, db: Session = Depends(get_db)):
    db_user = userOperation.check_if_user_exists(db, email=user.email, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return userOperation.create_user(db=db, user_=user)


# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.post('/v1/login')
def login(user: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # user = userOperation.get_user(db, username=token_data.username)
    user = userOperation.authenticate_user(db, user.username, user.password)

    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    """
    create_access_token supports an optional 'fresh' argument,
    which marks the token as fresh or non-fresh accordingly.
    As we just verified their username and password, we are
    going to mark the token as fresh here.
    """
    access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_type": "Bearer", "access_token": access_token, "refresh_token": refresh_token}


@app.post('/v1/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


# Basically Logout function
@app.delete('/v1/access-revoke')
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    jti = Authorize.get_raw_jwt()['jti']
    redis_conn.setex(jti, tokenSettings.access_expires, 'true')
    return {"status": "200", "message": "Access token has been revoke, logged out"}


# Endpoint for revoking the current users refresh token
@app.delete('/v1/refresh-revoke')
def refresh_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    jti = Authorize.get_raw_jwt()['jti']
    redis_conn.setex(jti, tokenSettings.refresh_expires, 'true')
    return {"detail": "Refresh token has been revoke"}


# Any valid JWT access token can access this endpoint
@app.get('/v1/protected')
def protected(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    userDetails = userOperation.get_user(db, current_user)
    return {"details": userDetails}


# Only fresh JWT access token can access this endpoint
@app.get('/v1/protected-fresh')
def protected_fresh(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

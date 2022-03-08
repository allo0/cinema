from datetime import timedelta
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, Form
from sqlalchemy.orm import Session
from starlette import status

import models.users.user_controller
from base.db import get_db
from models.auth.token import Token, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.users import user_model, user_controller

openRouter = APIRouter(
    tags=["Open api calls"],
    responses={404: {"description": "Not found"}},
)


@openRouter.get("/")
async def root():
    return {"message": "Hello World"}


@openRouter.post("/register")
def create_user(user: user_model.UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.check_if_user_exists(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Account already exists",
                            headers={"WWW-Authenticate": "Bearer"},
                            )

    return {"status": 200, "user_info": user_controller.create_user(db=db, user_=user)}


@openRouter.post("/auth/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), username: str = Form(...),
                                 password: Optional[str] = Form(None),
                                 user_id: Optional[str] = Form(None)):
    # user = models.users.user_controller.authenticate_user(db, form_data.username, form_data.password, user_id)
    user = models.users.user_controller.authenticate_user(db, username, password, user_id)
    if user == 418:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT,
                            detail="Google account not registered, go get a teapot",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

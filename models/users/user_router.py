from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from base.db import Base, engine, get_db
from main import get_current_active_user
from models.users.user_model import User, UserCreate, UserModel, UserUpdate

Base.metadata.create_all(bind=engine)
userRouter = SQLAlchemyCRUDRouter(
    schema=User,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    db_model=UserModel,
    db=get_db,
    prefix='user',
    delete_all_route=False,
    get_one_route=False,
    tags=['Users']

)


# @userRouter.post("")
# def create_user(user: user_model.UserCreate, db: Session = Depends(get_db)):
#     db_user = user_controller.check_if_user_exists(db, email=user.email, username=user.username)
#
#     if db_user:
#         return {"status": 4004, "user_info": {}}
#
#     return {"status": 200, "user_info": user_controller.create_user(db=db, user_=user)}

@userRouter.get("", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

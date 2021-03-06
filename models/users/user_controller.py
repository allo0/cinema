from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.open.open_controller import create_uiid
from models.users import user_model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, email: str):
    return db.query(user_model.UserModel) \
        .filter(
        user_model.UserModel.email == email) \
        .first()


def get_user_by_activation_code(db: Session, activation_code: str):
    return db.query(user_model.UserModel) \
        .filter(
        user_model.UserModel.activation_code == activation_code) \
        .first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_user_by_user_id(db: Session, user_id: str):
    return db.query(user_model.User).filter(user_model.User.user_id == user_id).first()


def check_if_user_exists(db: Session, email: str):
    return db.query(user_model.UserModel) \
        .filter(user_model.UserModel.email == email) \
        .first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user_: user_model.UserCreate):
    hashed_password = ''

    if user_.password:
        hashed_password = get_password_hash(user_.password)

    if not user_.user_id:
        db_user = user_model.UserModel(email=user_.email, user_id=user_.user_id, username=user_.username,
                                       firstName=user_.firstName, lastName=user_.lastName, photoUrl=user_.photoUrl,
                                       password=hashed_password, user_type=user_.user_type, is_verified=False,
                                       activation_code=create_uiid())

    else:
        db_user = user_model.UserModel(email=user_.email, user_id=user_.user_id, username=user_.username,
                                       firstName=user_.firstName, lastName=user_.lastName, photoUrl=user_.photoUrl,
                                       user_type=user_.user_type, is_verified=True,
                                       activation_code=create_uiid())

    db.add(db_user)
    db.commit()

    db.refresh(db_user)

    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: Optional[str] = None,
                      user_id: Optional[str] = None):
    user = get_user(db, email=email)

    if not user and not user_id:
        return False

    if user_id:
        if not user:
            return False
        if user_id != user.user_id:
            return 418

    if password and user.is_verified == 1:
        if not verify_password(password, user.password) and not user_id:
            return False
    elif password and user.is_verified == 0:
        return 401

    return user


def user_activation(db: Session, activation_code: str):
    user = get_user_by_activation_code(db=db, activation_code=activation_code)
    # db_user = user_model.UserUpdate(email=user.email, user_id=user.user_id, username=user.username,
    #                                firstName=user.firstName, lastName=user.lastName, photoUrl=user.photoUrl,
    #                                password=user.password, user_type=user.user_type, is_verified=True)
    if not user.is_verified:
        user.is_verified = True
        db.add(user)
        db.commit()

        db.refresh(user)
    return user

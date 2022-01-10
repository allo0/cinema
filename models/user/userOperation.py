from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.user import userSchema, userModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, email: str, username: Optional[str] = None):
    return db.query(userModel.User) \
        .filter(or_(userModel.User.email == email, userModel.User.username == username)) \
        .first()


def get_user_by_email(db: Session, email: str):
    return db.query(userModel.User).filter(userModel.User.email == email).first()


def check_if_user_exists(db: Session, email: str, username: str):
    return db.query(userModel.User) \
        .filter(or_(userModel.User.email == email, userModel.User.username == username)) \
        .first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(userModel.User).offset(skip).limit(limit).all()


def create_user(db: Session, user_: userSchema.UserCreate):
    hashed_password = get_password_hash(user_.password)
    db_user = userModel.User(email=user_.email, username=user_.username, firstName=user_.firstName, lastName=user_.lastName,
                             hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, username: str, password: str):
    user = get_user(db, email=email, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

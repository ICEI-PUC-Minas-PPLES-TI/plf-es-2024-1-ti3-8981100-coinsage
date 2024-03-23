from sqlalchemy.orm import Session

from src.models.db import user as userDB
from src.models.schemas import user


def get_user(db: Session, user_id: int):
    return db.query(userDB.User).filter(userDB.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(userDB.User).filter(userDB.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(userDB.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = userDB.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

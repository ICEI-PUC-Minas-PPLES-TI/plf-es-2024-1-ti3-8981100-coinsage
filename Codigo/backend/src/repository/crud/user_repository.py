from sqlalchemy.orm import Session

from src.models.db.user import UserModel
from src.models.schemas import user


def get_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user: user.UserCreate):
    db_user = UserModel(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

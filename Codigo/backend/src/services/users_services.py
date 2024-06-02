import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.db.user import UserModel
from src.models.schemas.user import UserCreate, UserResponse
from src.repository.crud import user_repository


class UserService:
    def __init__(self):
        self.repository = user_repository

    def create(self, db: Session, user: UserCreate) -> UserResponse:
        if self.user_exists(db, user):
            raise HTTPException(status_code=400, detail="User already exists")

        self.validate_user(user)

        user_created: UserModel = self.repository.create_user(db, user)
        return UserResponse(id=user_created.id, email=user_created.email, name=user_created.name)

    def user_exists(self, db: Session, user: UserCreate) -> bool:
        return self.repository.get_by_email(db, user.email) is not None

    def validate_user(self, user: UserCreate):
        self.validate_email(user.email)
        self.validate_password(user.password)

    def validate_email(self, email: str) -> bool:
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if re.match(pattern, email) is None:
            raise HTTPException(status_code=400, detail="Invalid email format")

    def validate_password(self, password: str) -> bool:
        if not len(password) >= 6:
            raise HTTPException(status_code=400, detail="Password must have at least 6 characters")

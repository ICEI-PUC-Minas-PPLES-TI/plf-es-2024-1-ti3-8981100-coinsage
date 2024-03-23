from sqlalchemy.orm import Session

from src.repository.crud.user_repository import get_user, create_user, get_users, get_user_by_email
from src.models.db.user import User as UserDB
from src.models.schemas.user import UserCreate, UserResponse
from src.repository.database import SessionLocal

class UserService:
    def __init__(self, session: Session):
        self.session = session
        pass

    def create_user(self, user: UserCreate) -> UserResponse:
        user_created: UserDB = create_user(self.session, user)
        user_response: UserResponse = UserResponse(**user_created.__dict__)
        return user_response

    def get_user(self, user_id: int) -> UserResponse:
        user: UserDB = get_user(self.session, user_id)
        user_response: UserResponse = UserResponse(**user.__dict__)
        return user_response
    
    def get_user_by_email(self, email: str) -> UserResponse:
        user: UserDB = get_user_by_email(self.session, email)
        user_response: UserResponse = UserResponse(**user.__dict__)
        return user_response
    
    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        users: list[UserDB] = get_users(self.session, skip, limit)
        users_response: list[UserResponse] = [UserResponse(**user.__dict__) for user in users]
        return users_response
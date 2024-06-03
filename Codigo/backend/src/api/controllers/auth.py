from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.user import UserCreate, UserResponse
from src.security.authentication import get_current_user
from src.services.authentication import AuthenticationService
from src.services.users_services import UserService

router = APIRouter()


@router.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthenticationService().authenticate(db, form_data)


@router.get("/current", response_model=UserResponse)
async def current_user(user: UserResponse = Depends(get_current_user)):
    return user


@router.post("/singin", response_model=UserResponse)
def sign_up(obj_in: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return UserService().create(db=db, user=obj_in)

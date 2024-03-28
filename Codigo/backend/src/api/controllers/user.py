import fastapi
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.user import UserCreate, UserResponse
from src.services.users_services import UserService

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="",
    name="users:create-user",
    response_model=UserResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate, db: Session = fastapi.Depends(get_db)) -> UserResponse:
    user_created = UserService(session=db).create_user(user)
    if user_created is None:
        raise fastapi.HTTPException(status_code=400, detail="Email already registered")
    return user_created


@router.get(
    path="/",
    name="users:get-all-users",
    response_model=list[UserResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def read_users(skip: int = 0, limit: int = 100, db: Session = fastapi.Depends(get_db)) -> list[UserResponse]:
    users = UserService(session=db).get_users(skip, limit)
    return users


@router.get(
    path="/{user_id}",
    name="users:get-user",
    response_model=UserResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def read_user(user_id: int, db: Session = fastapi.Depends(get_db)) -> UserResponse:
    user = UserService(session=db).get_user(user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user

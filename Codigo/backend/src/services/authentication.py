import logging
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.orm import Session

from src.config.manager import settings
from src.models.schemas.user import UserBase, UserCreate, UserLogin, UserResponse
from src.repository.crud import user_repository


class AuthenticationService:
    def __init__(self):
        self.repository = user_repository

    def check_operator(self, db: Session, user: UserLogin) -> UserCreate:
        model = self.repository.get_by_email(db, email=user.email)

        if not model:
            logger.error(f"User {user.email} not found")
            raise HTTPException(status_code=404, detail=f"User not found with email {user.email}")

        if not self.compare_passwords(user.password, model.password):
            logger.error(f"Invalid password for user {model.email}")
            raise HTTPException(status_code=401, detail="Invalid password")

        return UserCreate(**model.__dict__)

    def compare_passwords(self, entry: str, original: str) -> bool:
        return entry == original

    def authenticate(self, db: Session, user: OAuth2PasswordRequestForm) -> str:
        logger.info(f"Authenticating user {user.username}")

        user_found = self.check_operator(db, UserLogin(email=user.username, password=user.password))
        return self.generate_token(UserBase(email=user_found.email, name=user_found.name))

    def generate_token(self, user: UserBase) -> str:
        token = jwt.encode(
            payload={
                **user.model_dump(),
                "exp": datetime.now() + timedelta(days=settings.JWT_EXPIRE),
                "iat": datetime.now(),
            },
            algorithm=settings.JWT_ALGORITHM,
            key=settings.JWS_SECRET,
        )
        return token

    def decode_token(self, token: str, db: Session) -> UserResponse:
        try:
            payload = jwt.decode(token, settings.JWS_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user = self.repository.get_by_email(db=db, email=payload.get("email"))
            return UserResponse(**user.__dict__)
        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            raise HTTPException(status_code=401, detail="Error decoding token")

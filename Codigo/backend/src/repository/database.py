from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.manager import settings

# from fastapi_utils.session import FastAPISessionMaker


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL, )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

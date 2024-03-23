import loguru
from sqlalchemy import event

from src.repository.database import engine, Base, SessionLocal

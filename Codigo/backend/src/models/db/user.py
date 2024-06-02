from sqlalchemy import BigInteger, Column, String

from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=False)

import uuid

from sqlalchemy import Column, Integer, String, UUID

from .base import Base


class Setor(Base):
    __tablename__ = "setor"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=200))
    coinst_quantity = Column(Integer)

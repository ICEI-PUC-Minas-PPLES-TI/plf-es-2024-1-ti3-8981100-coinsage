import uuid

from sqlalchemy import Boolean, Column, Integer, String, UUID

from .base import Base


class Setor(Base):
    __tablename__ = "setor"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=500))
    title = Column(String(length=500))
    coins_quantity = Column(Integer)
    cmc_id = Column(Integer)
    active = Column(Boolean, default=True)

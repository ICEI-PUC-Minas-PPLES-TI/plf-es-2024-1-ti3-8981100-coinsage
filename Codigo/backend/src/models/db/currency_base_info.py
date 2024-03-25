import uuid
from typing import List

from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship

from .base import Base


class CurrencyBaseInfoModel(Base):
    __tablename__ = "currency_base_info"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(length=100), unique=True)
    cmc_id = Column(Integer)
    cmc_slug = Column(String(length=100))
    logo = Column(String(length=1000))
    name = Column(String(length=100))
    description = Column(String(length=5000))
    technical_doc: Column[List[str]] = Column(ARRAY(String(length=1000)), nullable=True)
    urls: Column[List[str]] = Column(ARRAY(String(length=1000)), nullable=True)
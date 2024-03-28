import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, NUMERIC, UUID
from sqlalchemy.orm import relationship

from ..base import Base


class ClosingPriceModel(Base):
    __tablename__ = "closing_price"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuid_currency_info = Column(UUID(as_uuid=True), ForeignKey("currency_base_info.uuid"))
    closing_price = Column(NUMERIC(precision=15, scale=8), nullable=False)  # type: ignore
    week = Column(DateTime, nullable=False)

    currency = relationship("CurrencyBaseInfoModel", back_populates="closing_prices")

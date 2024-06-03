import uuid

from sqlalchemy import Column, DateTime, ForeignKey, NUMERIC, UUID

from .base import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transaction"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quantity = Column(NUMERIC(precision=20, scale=8), nullable=True)  # type: ignore
    amount = Column(NUMERIC(precision=20, scale=8), nullable=True)  # type: ignore
    date = Column(DateTime, nullable=False)  # type: ignore
    price_on_purchase = Column(NUMERIC(precision=15, scale=8), nullable=False)  # type: ignore
    uuid_currency = Column(UUID(as_uuid=True), ForeignKey("currency_base_info.uuid"))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # type: ignore

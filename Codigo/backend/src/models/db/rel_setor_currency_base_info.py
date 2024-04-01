import uuid

from sqlalchemy import Column, ForeignKey, UUID

from .base import Base


class SetorCurrencyBaseInfo(Base):
    __tablename__ = "setor_currency_base_info"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuid_setor = Column(UUID(as_uuid=True), ForeignKey("setor.uuid"))
    uuid_currency = Column(UUID(as_uuid=True), ForeignKey("currency_base_info.uuid"))

import uuid

from sqlalchemy import Column, DateTime, UUID

from .base import Base


class Analysis(Base):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime)

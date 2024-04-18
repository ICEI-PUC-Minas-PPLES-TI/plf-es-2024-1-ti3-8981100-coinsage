import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, UUID

from .base import Base


class Analysis(Base):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # type: ignore
    date = Column(DateTime, default=datetime.now())  # type: ignore
    ended = Column(Boolean, default=False)  # type: ignore

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UUID

from .base import Base


class SectorInfoScheduleModel(Base):
    __tablename__ = "sector_info_schedule"
    id = Column(Integer, primary_key=True, index=True)
    last_update_time = Column(DateTime, default=datetime.now())
    next_scheduled_time = Column(DateTime, nullable=False)

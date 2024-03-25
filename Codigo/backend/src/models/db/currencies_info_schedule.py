from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

from .base import Base

class CurrenciesInfoScheduleModel(Base):
    __tablename__ = "currencies_info_schedule"
    id = Column(Integer, primary_key=True, index=True)
    last_update_time = Column(DateTime, default=datetime.now())
    next_scheduled_time = Column(DateTime, nullable=False)
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UUID

from .base import Base


class AnalysisInfoScheduleModel(Base):
    __tablename__ = "analysis_info_schedule"
    id = Column(Integer, primary_key=True, index=True)
    uuid_analysis = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"))
    last_update_time = Column(DateTime, default=datetime.now())
    next_scheduled_time = Column(DateTime, nullable=False)

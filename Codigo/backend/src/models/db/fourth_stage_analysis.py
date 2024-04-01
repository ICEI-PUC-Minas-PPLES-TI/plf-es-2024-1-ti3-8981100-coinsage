import uuid

from sqlalchemy import Boolean, Column, ForeignKey, NUMERIC, UUID

from .base import Base


class FourthStageAnalysisModel(Base):
    __tablename__ = "analysis_currency_stage_four"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuid_analysis = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"))
    uuid_currency = Column(UUID(as_uuid=True), ForeignKey("currency_base_info.uuid"))
    mon_semester_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    mon_quarter_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    mon_mon_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    mon_week_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    variation_consistent = Column(Boolean)

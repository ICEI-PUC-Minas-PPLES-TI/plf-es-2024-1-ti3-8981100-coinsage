import uuid

from sqlalchemy import Boolean, Column, ForeignKey, NUMERIC, UUID

from .base import Base


class SecondStageAnalysisModel(Base):
    __tablename__ = "analysis_currency_stage_two"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuid_analysis = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"))
    uuid_currency = Column(UUID(as_uuid=True), ForeignKey("currency_base_info.uuid"))
    year_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    semester_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    quarter_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    month_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    week_variation_per = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    variation_greater_bitcoin = Column(Boolean)

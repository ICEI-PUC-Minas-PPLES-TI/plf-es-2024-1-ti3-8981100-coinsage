import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, NUMERIC, UUID

from .base import Base


class FirstStageAnalysisModel(Base):
    __tablename__ = "analysis_currency_stage_one"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # type: ignore
    uuid_analysis = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"))
    uuid_currency = Column(UUID(as_uuid=True), ForeignKey("currency_base_info.uuid"))
    ranking = Column(Integer)  # type: ignore
    market_value = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    week_increase_percentage = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    increase_date = Column(DateTime)
    closing_price = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    last_week_closing_price = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    open_price = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    ema8 = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    ema8_greater_open = Column(Boolean)  # type: ignore
    ema8_less_close = Column(Boolean)  # type: ignore
    week_increase_volume = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    increase_volume_day = Column(DateTime)
    day_before_volume = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    volumes_relation = Column(NUMERIC(precision=15, scale=8))  # type: ignore
    expressive_volume_increase = Column(Boolean)  # type: ignore
    ema_aligned = Column(Boolean)  # type: ignore
    buying_signal = Column(Boolean)  # type: ignore
    today = Column(DateTime)

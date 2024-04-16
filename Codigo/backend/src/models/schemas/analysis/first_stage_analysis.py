from datetime import datetime
from typing import List
from uuid import UUID

from src.models.schemas.base import BaseSchemaModel
from src.models.schemas.sector import SectorRead


class AnalysisCurrencyInfo(BaseSchemaModel):
    symbol: str
    uuid: UUID
    logo: str
    main_sector: SectorRead


class FirstStageAnalysisResponse(BaseSchemaModel):
    currency: AnalysisCurrencyInfo
    week_increase_percentage: float | None
    valorization_date: datetime | None
    closing_price: float | None
    open_price: float | None
    last_week_closing_price: float | None
    ema8: float | None
    ema8_greater_open: bool | None
    ema8_less_close: bool | None

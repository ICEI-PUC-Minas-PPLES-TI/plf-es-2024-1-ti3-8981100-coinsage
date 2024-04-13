from datetime import datetime
from typing import List
from uuid import UUID

from src.models.schemas.base import BaseSchemaModel


class AnalysisCurrencyInfo(BaseSchemaModel):
    main_sector: str
    symbol: str
    logo: str


class FirstStageAnalysisResponse(BaseSchemaModel):
    currency: AnalysisCurrencyInfo
    week_increase_percentage: float | None
    valorization_date: datetime | None
    current_price: float | None

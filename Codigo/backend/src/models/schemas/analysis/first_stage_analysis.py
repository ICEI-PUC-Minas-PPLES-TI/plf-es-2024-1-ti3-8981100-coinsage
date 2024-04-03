from datetime import datetime
from typing import List
from uuid import UUID

from src.models.schemas.base import BaseSchemaModel
from src.models.schemas.currency_info import CurrencyInfo


class FirstStageAnalysisResponse(BaseSchemaModel):
    currency: CurrencyInfo
    week_incerae_percentage: float
    valorization_date: datetime
    current_price: float

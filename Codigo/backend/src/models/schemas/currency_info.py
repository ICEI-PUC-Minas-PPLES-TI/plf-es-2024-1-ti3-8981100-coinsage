from datetime import datetime
from typing import List
from uuid import UUID

from src.models.schemas.base import BaseSchemaModel


class CurrencyInfo(BaseSchemaModel):
    symbol: str
    cmc_id: int
    cmc_slug: str
    logo: str
    name: str
    description: str
    current_price: float
    _technical_doc: list[str]
    _urls: list[str]


class LastUpdate(BaseSchemaModel):
    time: datetime
    data: List[CurrencyInfo]


class CurrencyInfoResponse(BaseSchemaModel):
    next_update: datetime
    last_update: LastUpdate

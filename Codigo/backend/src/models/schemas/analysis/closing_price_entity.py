from datetime import datetime
from uuid import UUID

from ..base import BaseSchemaModel


class ClosingPriceEntity(BaseSchemaModel):
    uuid: UUID
    uuid_currency_info: UUID
    closing_price: float
    week: datetime


class ClosingPriceResponse(BaseSchemaModel):
    symbol: str
    closing_price: float
    week: datetime

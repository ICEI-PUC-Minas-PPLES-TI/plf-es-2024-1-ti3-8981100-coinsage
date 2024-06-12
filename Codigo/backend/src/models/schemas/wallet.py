from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel
from src.models.schemas.currency_info import SimpleCrypto


class BuyWalletCreate(BaseSchemaModel):
    crypto: str
    date: str = Field(
        ...,
        pattern="^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-[0-9]{4} (0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
        description="Data da compra da criptomoeda",
    )
    quantity: Annotated[Decimal, Field(..., max_digits=20, decimal_places=8, gt=0)] | None
    amount: Annotated[Decimal, Field(..., max_digits=20, decimal_places=8, gt=0)] | None
    price_on_purchase: Annotated[Decimal, Field(..., max_digits=15, decimal_places=8, gt=0)] | None

    @property
    def _date(self):
        return datetime.strptime(self.date, "%d-%m-%Y %H:%M")


class ProfitCompare(BaseSchemaModel):
    buy_date: datetime
    buy_price: Decimal
    compare_date: datetime
    current_price: Decimal
    buy_value: Decimal
    current_value: Decimal
    profit: Decimal


class ResponseProfitCompare(BaseSchemaModel):
    transaction_uuid: UUID
    crypto: SimpleCrypto
    profit: ProfitCompare


class CompleteWalletTransaction(BuyWalletCreate):
    uuid: UUID
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class CompleteWalletTransaction(BaseSchemaModel):
    uuid: UUID
    crypto: str
    date: datetime
    quantity: Decimal
    amount: Decimal
    price_on_purchase: Decimal
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True

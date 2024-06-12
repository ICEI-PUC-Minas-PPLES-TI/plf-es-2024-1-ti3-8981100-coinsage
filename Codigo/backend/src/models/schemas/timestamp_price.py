from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class TimestampPrice(BaseSchemaModel):
    crypto: str
    date: str = Field(
        ...,
        pattern="^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-[0-9]{4} ([0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9])$",
        description="Data da compra da criptomoeda",
    )

    @property
    def _date(self):
        return datetime.strptime(self.date, "%d-%m-%Y %H:%M")

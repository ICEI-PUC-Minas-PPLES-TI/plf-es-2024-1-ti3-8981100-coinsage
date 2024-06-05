from uuid import UUID

from src.models.schemas.base import BaseSchemaModel


class SectorRead(BaseSchemaModel):
    uuid: UUID
    title: str
    coins_quantity: int

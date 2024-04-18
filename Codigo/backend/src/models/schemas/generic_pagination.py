from typing import Optional

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class PaginatedResponse(BaseSchemaModel):
    total: int = Field(description="Number of items in the database")
    page: int = Field(description="Number of items in the current page")
    remaining: Optional[int] = Field(description="Number of items remaining in the database")

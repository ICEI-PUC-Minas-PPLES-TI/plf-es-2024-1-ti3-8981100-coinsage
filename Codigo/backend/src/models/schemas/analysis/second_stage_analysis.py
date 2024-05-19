from src.models.schemas.base import BaseSchemaModel


class VariationPerSchema(BaseSchemaModel):
    symbol: str
    year_variation_per: float | None
    semester_variation_per: float | None
    quarter_variation_per: float | None
    month_variation_per: float | None
    week_variation_per: float | None

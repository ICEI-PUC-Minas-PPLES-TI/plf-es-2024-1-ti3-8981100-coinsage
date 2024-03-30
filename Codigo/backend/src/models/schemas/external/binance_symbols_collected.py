from ..base import BaseSchemaModel


class BinanceSymbolsCollected(BaseSchemaModel):
    symbol: str
    base_asset: str
    quote_asset: str

from pydantic import BaseModel


class BinanceSymbolsCollected(BaseModel):
    symbol: str
    base_asset: str
    quote_asset: str

    class Config:
        from_attributes = True

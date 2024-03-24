from pydantic import BaseModel
        
class CurrencyInfo(BaseModel):
    symbol: str
    cmc_id: int
    cmc_slug: str
    logo: str
    name: str
    description: str
    technical_doc: list[str]
    urls: list[str]

    class Config:
        from_attributes = True

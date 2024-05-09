from decimal import Decimal

from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from src.models.schemas.timestamp_price import TimestampPrice
from src.repository.crud import currency_info_repository
from src.services.externals.binance_price_at_timestamp import BinancePriceAtTimestampService


class PriceAtTimestampService:
    def __init__(self):
        self.symbols_repository = currency_info_repository

    def get_price_by_date_time(self, packet: TimestampPrice, session: Session) -> Decimal:
        symbol = self.symbols_repository.get_currency_info_by_symbol(session, packet.crypto)
        if symbol is None:
            logger.error(f"Símbolo não encontrado: {packet.crypto}")
            raise HTTPException(status_code=404, detail="Criptomoeda não encontrada")

        try:
            return BinancePriceAtTimestampService().get_by_symbol(symbol=packet.crypto, date_time=packet._date)
        except Exception as e:
            logger.error(f"Erro ao buscar preço: {e}")
            raise HTTPException(status_code=404, detail="Preço não encontrado")

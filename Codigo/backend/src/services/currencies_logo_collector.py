import time
from typing import Any

from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.schemas.currency_info import CurrencyInfo
from src.repository.crud import currency_info_repository
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector
from src.services.externals.cmc_symbol_colletor import CmcSymbolCollector


class CurrenciesLogoCollector:
    def __init__(self, session: Session):
        self.session = session
        self.cmc_symbols: Any = None
        self.repository = currency_info_repository

    def _clear_table(self):
        self.repository.clear_table(self.session)

    def collect_symbols_info(self):
        self._clear_table()
        self.cmc_symbols = CmcSymbolCollector(BinanceSymbolCollector().get_base_assets_as_str()).get_symbols()
        start_time = time.time()
        for symbol in self.cmc_symbols:
            try:
                coin = self.cmc_symbols[symbol][0]
                if coin["symbol"] == "EUR":
                    continue
                self.repository.create_crypto(
                    self.session,
                    CurrencyInfo(
                        symbol=coin["symbol"],
                        cmc_id=coin["id"],
                        cmc_slug=coin["slug"],
                        urls=coin["urls"]["website"],
                        technical_doc=coin["urls"]["technical_doc"],
                        logo=coin["logo"],
                        name=coin["name"],
                        description=coin["description"],
                    ),
                )
            except Exception as e:
                logger.error(f"Error on [{symbol}]:\n{e}")

        logger.info(f"Parsing symbols took {(time.time() - start_time)/1000}ms")

    def get_cryptos(self):
        return self.repository.get_cryptos(self.session)

    def get_crypto(self, crypto_uuid: Uuid):
        return self.repository.get_crypto(self.session, crypto_uuid)

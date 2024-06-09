import datetime
import time
from typing import Any, List

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.currencies_info_schedule import CurrenciesInfoScheduleModel
from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.schemas.currency_info import CurrencyInfo, CurrencyInfoResponse, LastUpdate
from src.repository.crud import currencies_info_schedule_repository, currency_info_repository
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector
from src.services.externals.cmc_symbol_colletor import CmcSymbolCollector


class CurrenciesLogoCollector:
    def __init__(self, session: Session):
        self.session = session
        self.cmc_symbols: Any = None
        self.repository = currency_info_repository
        self.schedule_repository = currencies_info_schedule_repository

    def _clear_table(self):
        self.repository.clear_table(self.session)

    def get_crypto_by_name_or_symbol(self, match: str) -> List[dict]:
        founded = self.repository.get_by_match(self.session, match)
        return [
            {"symbol": crypto.symbol, "name": crypto.name, "uuid": crypto.uuid, "logo": crypto.logo}  # type: ignore
            for crypto in founded
        ]

    def get_all_reduced(self) -> List[dict[str, Any]]:
        founded = self.repository.get_by_match(self.session, "")
        return [
            {"symbol": crypto.symbol, "uuid": crypto.uuid, "name": crypto.name, "logo": crypto.logo}  # type: ignore
            for crypto in founded
        ]

    def manually_collect_symbols(self):
        currencies = self.repository.get_cryptos(self.session)
        if len(currencies) == 0:
            self.collect_symbols_info()
            return {"message": "No symbols found, starting new one"}
        if currencies[0].last_updated.date() != datetime.datetime.now().date():
            self.collect_symbols_info()
            return {"message": "Symbols are late, starting new one"}

        return {"message": "Symbols already updated"}

    def collect_symbols_info(self):
        self.cmc_symbols = CmcSymbolCollector(BinanceSymbolCollector().get_base_assets_as_str()).get_symbols()
        self.cmc_symbols.pop("EUR")

        start_time = time.time()
        for symbol in self.cmc_symbols:
            try:
                coin = self.cmc_symbols[symbol][0]
                symbol = self.repository.get_currency_info_by_symbol(self.session, coin["symbol"])

                if symbol is not None:
                    symbol.urls = coin["urls"]["website"]
                    symbol.technical_doc = coin["urls"]["technical_doc"]
                    symbol.logo = coin["logo"]
                    symbol.name = coin["name"]
                    symbol.description = coin["description"]
                    symbol.active = True
                    self.session.commit()
                    continue

                self.repository.create_crypto(
                    self.session,
                    CurrencyBaseInfoModel(
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

        self.repository.clear_inactive(self.session, self.cmc_symbols)

        logger.info(f"Parsing symbols took {(time.time() - start_time)/1000}ms")

        self.session.add(CurrenciesInfoScheduleModel(next_scheduled_time=self.calculate_next_time()))
        self.session.commit()

    def calculate_next_time(self) -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(days=1)

    def get_cryptos(self) -> CurrencyInfoResponse:
        cryptos: list[CurrencyBaseInfoModel] = self.repository.get_cryptos(self.session)
        last_update_info = self.schedule_repository.get_last_update(self.session)

        if last_update_info is not None:
            # Convert the cryptos list to CurrencyInfo
            converted_cryptos = [
                CurrencyInfo(
                    cmc_id=crypto.cmc_id,  # type: ignore
                    cmc_slug=crypto.cmc_slug,  # type: ignore
                    description=crypto.description,  # type: ignore
                    logo=crypto.logo,  # type: ignore
                    name=crypto.name,  # type: ignore
                    symbol=crypto.symbol,  # type: ignore
                    technical_doc=crypto.technical_doc,
                    urls=crypto.urls,
                )
                for crypto in cryptos
            ]

            # Create the response object using the correct attribute names:
            currency_info_response = CurrencyInfoResponse(
                last_update=LastUpdate(
                    time=getattr(last_update_info, "last_update_time"),
                    data=converted_cryptos,
                ),
                next_update=getattr(last_update_info, "next_scheduled_time"),
            )

            # Return the created response object:
            return currency_info_response

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma criptomoeda encontrada no banco de dados!"
        )

    def get_crypto(self, crypto_uuid: Uuid):
        return self.repository.get_crypto(self.session, crypto_uuid)

    def get_crypto_by_symbol(self, symbol: str):
        return self.repository.get_currency_info_by_symbol(self.session, symbol)

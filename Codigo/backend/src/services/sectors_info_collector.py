from typing import List

from loguru import logger
from sqlalchemy.orm import Session

from src.config.manager import settings
from src.models.db.rel_setor_currency_base_info import SetorCurrencyBaseInfo
from src.models.db.setor import Setor
from src.repository.crud import currency_info_repository, sector_info_repository
from src.services.externals.cmc_sectors_collector import CmcSectorsCollector
from src.utilities.runtime import show_runtime


class SectorsCollector:
    def __init__(self):
        self.repository = sector_info_repository
        self.symbols_repository = currency_info_repository
        self.external_collector = CmcSectorsCollector()
        self.MIN_CRYPOS_COUNT = settings.MIN_SECTOR_TOKENS_ACCEPTED

    def passed_min_coins(self, sector) -> bool:
        return sector["num_tokens"] >= self.MIN_CRYPOS_COUNT

    @show_runtime
    def collect(self, db_session: Session):
        cryptos = self.symbols_repository.get_cryptos(db_session)
        raw_sector_info = self.external_collector([crypto.symbol for crypto in cryptos])  # type: ignore
        for sector in raw_sector_info:
            sector_db = self.repository.get_sector_by_cmc_id(db_session, sector["cmc_id"])

            # New sector on the databse
            if sector_db is None and self.passed_min_coins(sector):
                logger.info(f"Creating new sector: {sector['name']}")
                new_sector = self.repository.create_sector(
                    db_session,
                    Setor(
                        name=sector["name"],
                        title=sector["title"],
                        coins_quantity=sector["num_tokens"],
                        cmc_id=sector["cmc_id"],
                    ),
                )
                self.add_coins_to_sector(db_session, new_sector, sector["symbols"])
                continue

            # Sector already exists on the database but it has less coins than the minimum required
            elif sector_db is not None and self.passed_min_coins(sector) is not True:
                logger.warning(f"Deactivating sector: {sector['name']}")
                sector_db.coins_quantity = sector["num_tokens"]
                sector_db.name = sector["name"]
                sector_db.title = sector["title"]
                self.repository.deactivate_sector(db_session, sector_db)
                self.remove_all_coins_from_sector(db_session, sector_db)
                continue

            # Sector already exists, just update the number of coins
            elif sector_db is not None:
                logger.info(f"Updating sector: {sector['name']}")
                sector_db.num_tokens = sector["num_tokens"]
                self.repository.update(db_session, sector_db)
                self.add_coins_to_sector(db_session, sector_db, sector["symbols"])
                continue

    def add_coins_to_sector(self, db_session: Session, sector: Setor, symbols: List[str]):
        symbols = self.exclude_existing_coins(db_session, sector, symbols)

        for symbol in symbols:
            crypto = self.symbols_repository.get_currency_info_by_symbol(db_session, symbol)
            if crypto is not None:
                relation = SetorCurrencyBaseInfo(uuid_setor=sector.uuid, uuid_currency=crypto.uuid)
                self.repository.add_coin_to_sector(db_session, relation)
                continue
            logger.warning(f"Coin {symbol} not found on the database")

    def remove_all_coins_from_sector(self, db_session: Session, sector: Setor):
        self.repository.remove_all_coins_from_sector(db_session, sector)

    def exclude_existing_coins(self, db_session: Session, sector: Setor, symbols: List[str]) -> List[str]:
        existing_coins = self.symbols_repository.get_coins_by_sector(db_session, sector.uuid)  # type: ignore
        for coin in existing_coins:
            if coin.symbol in symbols:
                symbols.remove(coin.symbol)  # type: ignore

        return symbols

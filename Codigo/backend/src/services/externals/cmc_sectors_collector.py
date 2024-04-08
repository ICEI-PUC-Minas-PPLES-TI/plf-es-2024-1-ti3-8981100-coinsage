import time
from datetime import datetime
from typing import List

from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from loguru import logger

from src.config.manager import settings
from src.utilities.runtime import show_runtime


class CmcSectorsCollector:
    def __init__(self):
        self.INTERVAL_CALL = 2  # in secods
        self.api = CoinMarketCapAPI(settings.CMC_API_KEY)
        self.sectors = []

    def __call__(self, symbols_list: List[str]):
        self.sectors = self._collect(symbols_list)
        return self.sectors

    @show_runtime
    def _collect(self, symbols_list: List[str]):
        for symbol in symbols_list:
            logger.debug(f"Collecting sector for {symbol}")  # TODO: Remove this line
            try:
                data = self.api.cryptocurrency_categories(symbol=symbol, limit=1000).data
                time.sleep(self.INTERVAL_CALL)
                if not data:
                    logger.error(f"No sector found for {symbol}")
                    continue
                for sector in data:
                    self.add_sector(sector, symbol)
            except Exception as e:
                logger.error(
                    f"""Error on symbol {symbol}:
                                   - Error: {type(e)}
                                   - Message: {str(e)}
                             """
                )
                raise e

        return self.sectors

    def add_sector(self, sector: dict, symbol: str):
        apend_time = datetime.now()
        for s in self.sectors:
            if s["name"] == sector["name"]:
                s["symbols"].append(symbol)
                logger.debug(f"Appended {symbol} to {sector['name']} in {datetime.now() - apend_time} seconds")
                return

        self.sectors.append(
            {
                "name": sector["name"],
                "title": sector["title"],
                "num_tokens": sector["num_tokens"],
                "cmc_id": sector["id"],
                "symbols": [symbol],
            }
        )

import time
from typing import Any, List

from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from loguru import logger

from src.config.manager import settings
from src.utilities.runtime import show_runtime


class CMCMarketCapCollector:
    def __init__(self):
        self.INTERVAL_CALL = 2  # in secods
        self.api = CoinMarketCapAPI(settings.CMC_API_KEY)
        self.start = 1
        self.last_call = None

    @show_runtime
    def collect(self, symbols: List[str]) -> List[Any]:
        results: List[Any] = []

        while len(results) < len(symbols):
            try:
                found = self.api.cryptocurrency_listings_latest(limit=200, start=self.start).data
                results.extend(self._get_symbols(found, symbols))
                self.start += 200
            except CoinMarketCapAPIError as error:
                logger.error(f"Error on collect CMC market caps: {error.rep.error_message}")
                raise error

            time.sleep(self.INTERVAL_CALL)

        return results

    def _get_symbols(self, found: List[dict], expected: List[str]) -> List[dict]:
        extracted = []
        for found_symbol in found:
            if found_symbol["symbol"] in expected:
                extracted.append(found_symbol)
        return extracted

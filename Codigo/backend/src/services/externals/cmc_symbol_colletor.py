import time
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from loguru import logger

from src.config.manager import settings

class CmcSymbolCollector:
    def __init__(self, symbols_list: str):
        self.api = CoinMarketCapAPI(settings.CMC_API_KEY)
        start_time = time.time()
        self.symbols = self._collect(symbols_list)
        logger.info(f'Collecting {len(self.symbols)} symbols from CoinMarketCap took {(time.time() - start_time)/1000}ms')
        
    def _collect(self, symbols_list: str):
        try:
            return self.api.cryptocurrency_info(symbol=symbols_list).data
        except CoinMarketCapAPIError as error:
            logger.error(f'Error message: {error.rep.error_message}')
            
            invalid_symbols = error.rep.error_message.split(': ')[1].replace('"', '').split(',')
            for symbol in invalid_symbols:
                symbols_list = symbols_list.replace(f'{symbol},', '')
            return self._collect(symbols_list)
        except Exception as e:
            logger.error(f'Error on [{symbols_list}]:\n{e}')
            raise e
        
    def get_symbols(self):
        return self.symbols
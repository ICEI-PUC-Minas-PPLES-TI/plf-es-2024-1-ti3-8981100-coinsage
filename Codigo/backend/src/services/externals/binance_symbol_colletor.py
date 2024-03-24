import time
from binance.spot import Spot
from loguru import logger

from src.models.schemas.external.binance_symbols_collected import BinanceSymbolsCollected

class BinanceSymbolCollector:
    def __init__(self):
        self.DEFAULT_QUOTE_ASSET = 'USDT'
        self.symbols: list[BinanceSymbolsCollected] = self._parse_symbols(self._collect_from_binance())

    def _collect_from_binance(self):
        star_time = time.time()
        symbols = Spot().exchange_info()['symbols']
        logger.info(f'Collecting symbols {len(symbols)} from Binance took {(time.time() - star_time)}ms')
        return symbols
    
    def _parse_symbols(self, symbols) -> list[BinanceSymbolsCollected]:
        return [
            BinanceSymbolsCollected(
                symbol=crypto_info['symbol'],
                base_asset=crypto_info['baseAsset'],
                quote_asset=crypto_info['quoteAsset']
            )
            for crypto_info in symbols
            if crypto_info['quoteAsset'] == self.DEFAULT_QUOTE_ASSET and crypto_info['status'] == 'TRADING'
        ]
    
    def get_symbols(self) -> list[BinanceSymbolsCollected]:
        return self.symbols
    
    def get_base_assets(self) -> set[str]:
        return {i.base_asset for i in self.symbols}
    
    def get_base_assets_as_str(self) -> str:
        return ','.join(symbol.base_asset for symbol in self.symbols)
    
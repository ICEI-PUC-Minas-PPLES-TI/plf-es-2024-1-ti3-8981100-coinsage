from sqlalchemy.orm import Session

from src.repository.crud import currency_info_repository, first_stage_repository
from src.services.externals.binance_closing_price_colletor import BinanceClosingPriceColletor
from src.services.sectors_info_collector import SectorsCollector


class DailyVolumeService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = first_stage_repository
        self.symbols_repository = currency_info_repository
        self.sectors_service = SectorsCollector()
        self.binance_closing_price_colletor = BinanceClosingPriceColletor()

    def get_day_volume(self):
        rolling_window_size = []
        symbols_str = [symbol.symbol for symbol in self.symbols_repository.get_cryptos(self.session)]
        splited_symbols_list = self._split_symbol_list(symbols_str=symbols_str)
        for symbols in splited_symbols_list:
            rolling_window_size.append(self.binance_closing_price_colletor.get_rolling_window_price(symbols=symbols))

    def _split_symbol_list(self, symbols_str: list):
        return [symbols_str[i : i + 200] for i in range(0, len(symbols_str), 200)]

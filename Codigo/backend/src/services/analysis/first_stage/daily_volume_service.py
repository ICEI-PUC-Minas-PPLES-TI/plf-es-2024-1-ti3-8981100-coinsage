import logging

from sqlalchemy.orm import Session

from src.services.externals.binance_closing_price_colletor import BinanceClosingPriceColletor
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector

logger = logging.getLogger(__name__)


class DailyVolumeService:
    def __init__(self, session: Session):
        self.session = session
        self.binance_closing_price_colletor = BinanceClosingPriceColletor()
        self.binance_symbol_collector = BinanceSymbolCollector()

    def get_day_volume(self) -> list:
        """
        Fetches and returns a list of current day trading volumes for each symbol batch, computed over a rolling window.

        Returns:
        - list: A list containing rolling window prices for batches of symbols.
        """
        rolling_window_size = []
        all_symbols = self.binance_symbol_collector.get_symbols()
        splited_symbols_list = self._split_symbol_list(all_symbols=all_symbols)
        for symbols in splited_symbols_list:
            rolling_window_size.append(self.binance_closing_price_colletor.get_rolling_window_price(symbols=symbols))
        return rolling_window_size

    def get_last_valuation_of_volume(self) -> list:
        """
        Evaluates and tracks the changes in volume over the last 7 days for each asset, identifying if today's volume has exceeded the past volumes.

        Returns:
        - list: A list of dictionaries where each dictionary contains the last valuation data and today's volume data for each symbol.
        """
        valuation_result = []
        rolling_windows_size_today = self.get_day_volume()
        day = 1
        for set_volume in rolling_windows_size_today:
            for volume in set_volume:
                asset_info = self.binance_closing_price_colletor.get_rolling_window_price(
                    symbol=volume["symbol"], window_size="{day}d".format(day=day)
                )  # type: ignore

                while not asset_info[0]["volume"] > volume["volume"]:
                    day += 1
                    if day > 7:
                        day = 1
                        logger.info(f"""In the last week the symbol: {volume["symbol"]} didn't appreciate.""")  # type: ignore[code]
                        break
                    asset_info = self.binance_closing_price_colletor.get_rolling_window_price(
                        symbols=[volume["symbol"]], window_size="{day}d".format(day=day)
                    )

                valuation_result.append({"last_valuation": asset_info, "today_volume": volume})
                day = 1
        logger.info(f"The valuation volumes were collected successful.")
        return valuation_result

    def _split_symbol_list(self, all_symbols: list) -> list:
        """
        Splits the list of all symbols into smaller batches of 100 symbols each for more manageable processing.

        Parameters:
        - all_symbols (list): A list of all trading symbols.

        Returns:
        - list: A list of lists, where each sublist contains up to 100 symbols.
        """
        return [[symbol.symbol for symbol in all_symbols[i : i + 100]] for i in range(0, len(all_symbols), 100)]

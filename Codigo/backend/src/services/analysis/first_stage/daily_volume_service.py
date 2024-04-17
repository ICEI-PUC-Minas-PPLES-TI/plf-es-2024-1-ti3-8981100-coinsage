import logging
from datetime import datetime, timedelta

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

    def get_last_volume_valuation(self) -> list:
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

                while not asset_info["volume"] > volume["volume"]:
                    day += 1
                    if day > 7:
                        day = 1
                        logger.info(f"In the last week the symbol: {volume['symbol']} didn't appreciate.")  # type: ignore
                        break
                    asset_info = self.binance_closing_price_colletor.get_rolling_window_price(
                        symbols=[volume["symbol"]], window_size="{day}d".format(day=day)
                    )

                valuation_result.append({"last_valuation": asset_info, "today_volume": volume})
                day = 1
        logger.info(f"The valuation volumes were collected successful.")
        return valuation_result

    def get_day_before_valuation(self) -> list:
        """
        Retrieves the valuation from the day before for each asset in the last volume valuation.

        Returns:
        - list: A list of valuation data for each symbol.
        """
        last_volume_valuation = self.get_last_volume_valuation()
        for volume in last_volume_valuation:
            volume_last_valuation = volume["last_valuation"]
            day = datetime.fromtimestamp(volume_last_valuation["closeTime"]).day + 1
            if day == 8:
                logging.info(f"The symbol {volume_last_valuation['symbol']} has not day before valuation")  # type: ignore
                continue
            last_volume_valuation.append(
                self.binance_closing_price_colletor.get_rolling_window_price(
                    symbols=[volume_last_valuation["symbol"]], window_size="{day}d".format(day=day)
                )
            )  # type: ignore
        return last_volume_valuation
    
    def get_increase_valuation_percentage(self)-> list:
        """
        Calculates the percentage increase in valuation for each symbol from the previous day's valuation to today.

        Returns:
        - list: A list of dictionaries, each containing the symbol and its increase percentage.
        """
        valuation_percentage = []
        last_volume_valuation = self.get_last_volume_valuation()
        for volume in last_volume_valuation:
            increase_percentage = self._calculate_valuation_percentage(volume)
            valuation_percentage.append(
                {"symbol":volume["last_valuation"]["symbol"], "increase_percentage":increase_percentage}
            )
        return valuation_percentage
    
    def get_valuation_date(self) -> list:
        """
        Retrieves the valuation date for each symbol from the rolling windows of today.

        Returns:
        - list: A list of dictionaries, each containing the symbol and its valuation date.
        """
        valuation_date = []
        rolling_windows_size_today = self.get_day_volume()
        for set_volume in rolling_windows_size_today:
            for volume in set_volume:
                valuation_date.append(
                    {"symbol": volume["symbol"], "valuation_date": datetime.fromtimestamp(volume["closeTime"])}
                )
        return valuation_date

    def _calculate_valuation_percentage(self, volume: dict) -> float:
        """
        Helper function to calculate the increase percentage based on volumes.

        Parameters:
        - volume (dict): Dictionary containing volume data for today and the last valuation.

        Returns:
        - float: The calculated increase percentage.
        """
        increase_percentage = (volume["last_valuation"]["volume"] / volume["today_volume"]["volume"]) * 100
        return increase_percentage

    def _split_symbol_list(self, all_symbols: list) -> list:
        """
        Splits the list of all symbols into smaller batches of 100 symbols each for more manageable processing.

        Parameters:
        - all_symbols (list): A list of all trading symbols.

        Returns:
        - list: A list of lists, where each sublist contains up to 100 symbols.
        """
        return [[symbol.symbol for symbol in all_symbols[i : i + 100]] for i in range(0, len(all_symbols), 100)]

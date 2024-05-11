# agg_trades
from datetime import datetime
from decimal import Decimal

from binance.spot import Spot
from loguru import logger


class BinancePriceAtTimestampService:
    def __init__(self):
        self.DEFAULT_QUOTE_ASSET = "USDT"

    def get_by_symbol(self, symbol: str, date_time: datetime) -> Decimal:
        date_time = date_time.replace(second=0, microsecond=0)  # Set seconds and microseconds to zero
        start_time = int(date_time.timestamp() * 1000)
        end_time = start_time + 30000
        values = Spot().agg_trades(symbol=f"{symbol}USDT", startTime=start_time, endTime=end_time)
        price = values[int(len(values) / 2)]["p"]
        return Decimal(price)

from typing import List

from src.services.analysis.first_stage.market_cap_service import MarketCapService
from src.services.externals import CMCMarketCapCollector


def test_call_with_symbols_list_without_errors():
    collector = CMCMarketCapCollector()
    symbols_list = ["BTC", "ETH", "LTC", "XRP", "ADA", "DOGE", "BNB", "DOT", "UNI", "LINK"]
    market_caps = collector.collect(symbols_list)

    assert isinstance(market_caps, List)
    assert len(market_caps) == len(symbols_list)

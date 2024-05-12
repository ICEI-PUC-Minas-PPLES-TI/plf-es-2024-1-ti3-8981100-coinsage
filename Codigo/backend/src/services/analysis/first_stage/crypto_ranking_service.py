from uuid import UUID

from loguru import logger
from sqlalchemy.orm import Session

from src.services.externals.binance_closing_price_colletor import BinanceClosingPriceColletor
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector
from src.services.externals.cmc_market_cap_collector import CMCMarketCapCollector
from src.repository.crud.first_stage_repository import update_ranking


class CryptoRankingService:

    def __init__(self, session: Session):
        self.session = Session
        self.binance_collector = BinanceClosingPriceColletor
        self.symbol_collector = BinanceSymbolCollector
        self.cmc_collector = CMCMarketCapCollector


    def collect_rankings(self, analysis_uuid: UUID):
        binance_symbols = self.symbol_collector.get_symbols()
        symbols = [symbol.symbol for symbol in binance_symbols if "USDT" in symbol.symbol]

        binance_data = self.binance_collector.collect(symbols, "1d", 1)
        cmc_data = self.binance_collector.collect(symbols)

        rankings = self.calculate_rankings(binance_data, cmc_data)

        for symbol, ranking in rankings.items():
            update_ranking(self.session, symbol, ranking, analysis_uuid)
    

    def calculate_rankings(self, binance_data: list, cmc_data: list):
        rankings = {}
        for cmc_entry in cmc_data:
            symbol = cmc_entry["symbol"]
            market_cap = cmc_entry.get("market_cap")
            closing_price = binance_data.get(symbol, {}).get("closing_price")

            if market_cap and closing_price:
                rankings[symbol] = market_cap / closing_price
            
        return rankings

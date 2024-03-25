import unittest

from src.models.schemas.external.binance_symbols_collected import BinanceSymbolsCollected
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector


class TestBinanceSymbolCollector(unittest.TestCase):
    def setUp(self):
        self.DEFAULT_QUOTE_ASSET = "USDT"
        self.DEFAULT_SYMBOLS_STATUS = "TRADING"
        self.TOTAL_BINANCE_SYMBOLS = 2550
        self.TOTAL_TRADING_USDT_COINS = 377
        self.cut = BinanceSymbolCollector()

    def test_should_succesfully_collect_binance_symbols(self):
        response = self.cut._collect_from_binance()

        self.assertEquals(len(response), self.TOTAL_BINANCE_SYMBOLS)
        self.assertTrue(all(key in response[0].keys() for key in ["symbol", "baseAsset", "quoteAsset"]))

    def test_should_succesfully_parse_symbols(self):
        symbols = self.cut._collect_from_binance()
        response = self.cut._parse_symbols(symbols)

        self.assertEqual(len(response), self.TOTAL_TRADING_USDT_COINS)
        self.assertTrue(all(isinstance(item, BinanceSymbolsCollected) for item in response))
        self.assertTrue(all(item.quote_asset == self.DEFAULT_QUOTE_ASSET for item in response))

    def test_should_return_symbols_list_correctly(self):
        response = self.cut.get_symbols()

        self.assertGreater(len(response), 0)
        self.assertTrue(all(isinstance(item, BinanceSymbolsCollected) for item in response))

    def test_should_return_base_assets_str_correctly(self):
        symbols = self.cut.get_symbols()
        response = self.cut.get_base_assets_as_str()

        self.assertIsInstance(response, str)
        self.assertTrue(all(item.base_asset in response for item in symbols))

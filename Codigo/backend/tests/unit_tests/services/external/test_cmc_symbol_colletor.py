import unittest

from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector
from src.services.externals.cmc_symbol_colletor import CmcSymbolCollector


class TestCmcSymbolColletor(unittest.TestCase):
    def setUp(self):
        self.cut = CmcSymbolCollector(BinanceSymbolCollector().get_base_assets_as_str())
        self.TOTAL_CMC_SYMBOLS = 374  # Counting EUR as well

    def test_should_succesfully_collect_cmc_symbols(self):
        response = self.cut.get_symbols()

        self.assertEquals(len(response), self.TOTAL_CMC_SYMBOLS)

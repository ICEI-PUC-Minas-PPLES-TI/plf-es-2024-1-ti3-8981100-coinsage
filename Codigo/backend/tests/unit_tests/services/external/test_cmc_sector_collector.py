import pytest
from coinmarketcapapi import CoinMarketCapAPIError

from src.services.externals.cmc_sectors_collector import CmcSectorsCollector


# @pytest.mark.skip
def test_call_with_symbols_list_without_errors():
    collector = CmcSectorsCollector()
    symbols_list = ["BTC", "ETH", "LTC"]
    sectors = collector(symbols_list)
    assert isinstance(sectors, list)
    for sector in sectors:
        assert "name" in sector
        assert "title" in sector
        assert "num_tokens" in sector
        assert "cmc_id" in sector
        assert "symbols" in sector


# @pytest.mark.skip
def test_handle_empty_input_symbols_list():
    collector = CmcSectorsCollector()
    symbols_list = []  # type: ignore
    sectors = collector(symbols_list)
    assert isinstance(sectors, list)
    assert len(sectors) == 0


# @pytest.mark.skip
def test_handle_unkown_symbol():
    collector = CmcSectorsCollector()
    symbols_list = ["UNKOWN"]
    try:
        collector(symbols_list)
    except CoinMarketCapAPIError as e:
        assert 'Invalid value for "symbol": "UNKOWN"' in str(e)


# @pytest.mark.skip
def test_handle_empty_api_response(mocker):
    mocker.patch("coinmarketcapapi.CoinMarketCapAPI.cryptocurrency_categories", return_value=None)

    collector = CmcSectorsCollector()
    symbols_list = ["BTC"]
    try:
        collector(symbols_list)
    except AttributeError as e:
        assert "NoneType" in str(e)


# @pytest.mark.skip
def test_cmc_api_rate_limit(mocker):
    mocker.patch("time.sleep")
    symbols_list = ["BTC"] * 31
    collector = CmcSectorsCollector()
    try:
        collector(symbols_list)
    except CoinMarketCapAPIError as e:
        assert "You've exceeded your API Key's" in str(e)


# @pytest.mark.skip
def test_should_not_raise_rate_limit_request_error():
    collector = CmcSectorsCollector()
    symbols_list = ["BTC"] * 70
    sectors = collector(symbols_list)

    assert len(sectors) > 0

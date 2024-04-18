import time

import pandas
import pytest

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.services.analysis.first_stage.ema_calculator_service import EmaCalculatorService


# calculate EMA for a single symbol, timeframe, and EMA size
def test_calculate_ema_single():
    # Arrange
    service = EmaCalculatorService()
    symbols = [
        CurrencyBaseInfoModel(
            symbol="BTC",
            cmc_id=1,
            cmc_slug="bitcoin",
            logo="https://bitcoin.com",
            name="Bitcoin",
            description="The first cryptocurrency",
            technical_doc=["https://bitcoin.com/technical"],
            urls=["https://bitcoin.com"],
        )
    ]
    timeframe = "1w"
    ema_size = 8

    # Act
    result = service.calculate(symbols, timeframe, ema_size)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["symbol"] == "BTC"
    assert result[0]["timeframe"] == "1w"
    assert result[0]["ema_size"] == 8
    assert isinstance(result[0]["ema_values"], pandas.DataFrame)


# calculate EMA for non existent symbol
def test_calculate_ema_nonexistent_symbol():
    # Arrange
    service = EmaCalculatorService()
    symbols = [CurrencyBaseInfoModel(symbol="NOEXT")]
    timeframe = "1w"
    ema_size = 8

    # Act
    result = service.calculate(symbols, timeframe, ema_size)

    # Assert
    assert len(result) == 0
    assert isinstance(result, list)


# calculate EMA for multiple symbols, same timeframe, and same EMA size
def test_calculate_ema_multiple_symbols():
    # Arrange
    service = EmaCalculatorService()
    symbols = [CurrencyBaseInfoModel(symbol="BTC"), CurrencyBaseInfoModel(symbol="ETH")]
    timeframe = "1w"
    ema_size = 21

    # Act
    result = service.calculate(symbols, timeframe, ema_size)

    # Assert
    assert len(result) == 2
    symbol = ["BTC", "ETH"]
    for item in result:
        assert item["timeframe"] == "1w"
        assert item["ema_size"] == 21
        assert isinstance(item["ema_values"], pandas.DataFrame)
        assert item["symbol"] in ["BTC", "ETH"]
        symbol.remove(item["symbol"])


@pytest.mark.skip()
def test_runtime_for_different_quantities():
    # Arrange
    service = EmaCalculatorService()
    symbols = [
        CurrencyBaseInfoModel(symbol="BTC"),
        CurrencyBaseInfoModel(symbol="ETH"),
        CurrencyBaseInfoModel(symbol="LTC"),
        CurrencyBaseInfoModel(symbol="ADA"),
        CurrencyBaseInfoModel(symbol="BNB"),
        CurrencyBaseInfoModel(symbol="DOGE"),
    ]
    less_symbols = [CurrencyBaseInfoModel(symbol="BTC"), CurrencyBaseInfoModel(symbol="ETH")]

    # Act
    start_time_symbols = time.time()
    result = service.calculate(symbols, "1w", 21)
    diff_time_symbols = time.time() - start_time_symbols
    start_time_less_symbols = time.time()
    result_less = service.calculate(less_symbols, "1w", 21)
    diff_time_less_symbols = time.time() - start_time_less_symbols

    # Assert
    assert diff_time_symbols == pytest.approx(diff_time_less_symbols, 2)

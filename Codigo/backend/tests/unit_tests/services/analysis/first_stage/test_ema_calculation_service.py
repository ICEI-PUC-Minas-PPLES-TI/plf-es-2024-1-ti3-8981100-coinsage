import pytest

from src.models.db.analysis import Analysis
from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.services.analysis.first_stage.ema_calculator_service import EmaCalculatorService
from src.services.currencies_info_collector import CurrenciesLogoCollector
from tests.db.db_fixture import test_session


def test_successfully_calulate_all_emas_crossovers(test_session):
    currency_service = CurrenciesLogoCollector(test_session)
    currency_service.collect_symbols_info()
    symbols = currency_service.get_cryptos().last_update.data
    symbols = symbols[:5]
    # symbols = [symbol for symbol in symbols if symbol.symbol == 'BTC']

    fake_analysis = Analysis()
    test_session.add(fake_analysis)
    test_session.commit()
    test_session.refresh(fake_analysis)

    for symbol in symbols:
        current_week = FirstStageAnalysisModel(
            uuid_analysis=fake_analysis.uuid,
            uuid_currency=test_session.query(CurrencyBaseInfoModel)
            .filter(CurrencyBaseInfoModel.symbol == symbol.symbol)
            .first()
            .uuid,
            closing_price=None,
            open_price=None,
            last_week_closing_price=None,
            today=None,
        )
        test_session.add(current_week)
        test_session.commit()

    result = EmaCalculatorService().calculate_crossovers(test_session, symbols, fake_analysis.uuid)

    assert result is None

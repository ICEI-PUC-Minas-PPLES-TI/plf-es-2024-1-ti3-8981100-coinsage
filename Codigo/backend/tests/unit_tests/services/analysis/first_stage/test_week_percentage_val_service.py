from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from src.models.db.analysis import Analysis
from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.services.analysis.first_stage.closing_price_service import ClosingPriceService
from src.services.analysis.first_stage.week_percentage_val_service import WeekPercentageValorizationService
from tests.db.db_fixture import test_session


def test_week_percentage_positive_valorization_calculated_correctly(test_session):
    fake_currency = CurrencyBaseInfoModel(
        symbol="BTC",
        cmc_id=1,
        cmc_slug="bitcoin",
        logo="https://bitcoin.com",
        name="Bitcoin",
        description="The first cryptocurrency",
        technical_doc=["https://bitcoin.com/technical"],
        urls=["https://bitcoin.com"],
    )

    test_session.add(fake_currency)
    test_session.commit()
    test_session.refresh(fake_currency)

    fake_analysis = Analysis()
    test_session.add(fake_analysis)
    test_session.commit()
    test_session.refresh(fake_analysis)

    today_date = datetime.now()
    last_week_date = today_date - timedelta(days=7)

    fake_first_stage_analysis_last_week = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency.uuid, today=last_week_date, closing_price=1000.0
    )

    test_session.add(fake_first_stage_analysis_last_week)
    test_session.commit()
    test_session.refresh(fake_first_stage_analysis_last_week)

    fake_first_stage_analysis_current_week = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency.uuid, today=today_date, closing_price=1100.0
    )

    test_session.add(fake_first_stage_analysis_current_week)
    test_session.commit()
    test_session.refresh(fake_first_stage_analysis_current_week)

    # Act
    sut = WeekPercentageValorizationService(
        session=test_session, closing_price_service=ClosingPriceService(session=test_session)
    )

    symbol = "BTC"
    result = sut._calculate_week_percentage_valorization(symbol)

    # Assert
    assert result == 10.0


def test_week_percentage_negative_valorization_calculated_correctly(test_session):
    fake_currency = CurrencyBaseInfoModel(
        symbol="BTC",
        cmc_id=1,
        cmc_slug="bitcoin",
        logo="https://bitcoin.com",
        name="Bitcoin",
        description="The first cryptocurrency",
        technical_doc=["https://bitcoin.com/technical"],
        urls=["https://bitcoin.com"],
    )

    test_session.add(fake_currency)
    test_session.commit()
    test_session.refresh(fake_currency)

    fake_analysis = Analysis()
    test_session.add(fake_analysis)
    test_session.commit()
    test_session.refresh(fake_analysis)

    today_date = datetime.now()
    last_week_date = today_date - timedelta(days=7)

    fake_first_stage_analysis_last_week = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency.uuid, today=last_week_date, closing_price=1100.0
    )

    test_session.add(fake_first_stage_analysis_last_week)
    test_session.commit()
    test_session.refresh(fake_first_stage_analysis_last_week)

    fake_first_stage_analysis_current_week = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency.uuid, today=today_date, closing_price=1000.0
    )

    test_session.add(fake_first_stage_analysis_current_week)
    test_session.commit()
    test_session.refresh(fake_first_stage_analysis_current_week)

    # Act
    sut = WeekPercentageValorizationService(
        session=test_session, closing_price_service=ClosingPriceService(session=test_session)
    )

    symbol = "BTC"
    result = sut._calculate_week_percentage_valorization(symbol)

    # Assert
    assert result == pytest.approx(result, -10)


def test_calculate_all_week_percentage_valorization(mocker, test_session):
    # Arrange
    fake_currency1 = CurrencyBaseInfoModel(
        symbol="BTC",
        cmc_id=1,
        cmc_slug="bitcoin",
        logo="https://bitcoin.com",
        name="Bitcoin",
        description="The first cryptocurrency",
        technical_doc=["https://bitcoin.com/technical"],
        urls=["https://bitcoin.com"],
    )
    fake_currency2 = CurrencyBaseInfoModel(
        symbol="ETH",
        cmc_id=2,
        cmc_slug="ethereum",
        logo="https://ethereum.com",
        name="Ethereum",
        description="The second cryptocurrency",
        technical_doc=["https://ethereum.com/technical"],
        urls=["https://ethereum.com"],
    )

    test_session.add_all([fake_currency1, fake_currency2])
    test_session.commit()

    fake_analysis = Analysis()
    test_session.add(fake_analysis)
    test_session.commit()

    today_date = datetime.now()
    last_week_date = today_date - timedelta(days=7)

    fake_first_stage_analysis_last_week_btc = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency1.uuid, today=last_week_date, closing_price=1000.0
    )
    fake_first_stage_analysis_last_week_eth = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency2.uuid, today=last_week_date, closing_price=2000.0
    )

    test_session.add_all([fake_first_stage_analysis_last_week_btc, fake_first_stage_analysis_last_week_eth])
    test_session.commit()

    fake_first_stage_analysis_current_week_btc = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency1.uuid, today=today_date, closing_price=1100.0
    )
    fake_first_stage_analysis_current_week_eth = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency2.uuid, today=today_date, closing_price=2200.0
    )

    test_session.add_all([fake_first_stage_analysis_current_week_btc, fake_first_stage_analysis_current_week_eth])
    test_session.commit()

    mocker.patch.object(
        ClosingPriceService,
        "get_closing_price_by_symbol",
        return_value=[fake_first_stage_analysis_last_week_btc, fake_first_stage_analysis_current_week_btc],
    )

    sut = WeekPercentageValorizationService(
        session=test_session, closing_price_service=ClosingPriceService(session=test_session)
    )

    symbols = ["BTC", "ETH"]

    # Act
    result = sut.calculate_all_week_percentage_valorization(symbols)
    eth_result = [x for x in result if x.uuid_currency == fake_currency2.uuid]
    btc_result = [x for x in result if x.uuid_currency == fake_currency1.uuid]

    # Assert
    assert result is not None
    assert len(result) == 4
    assert btc_result[1].week_increase_percentage == 10.0
    assert btc_result[0].week_increase_percentage == None
    assert btc_result[1].today == today_date
    assert btc_result[0].today == last_week_date
    assert eth_result[1].week_increase_percentage == 10.0
    assert eth_result[0].week_increase_percentage == None
    assert eth_result[1].today == today_date
    assert eth_result[0].today == last_week_date


def test_update_last(test_session):
    # Arrange
    fake_currency = CurrencyBaseInfoModel(
        symbol="BTC",
        cmc_id=1,
        cmc_slug="bitcoin",
        logo="https://bitcoin.com",
        name="Bitcoin",
        description="The first cryptocurrency",
        technical_doc=["https://bitcoin.com/technical"],
        urls=["https://bitcoin.com"],
    )

    test_session.add(fake_currency)
    test_session.commit()
    test_session.refresh(fake_currency)

    fake_analysis = Analysis()
    test_session.add(fake_analysis)
    test_session.commit()
    test_session.refresh(fake_analysis)

    today_date = datetime.now()
    last_week_date = today_date - timedelta(days=7)

    fake_first_stage_analysis_last_week = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency.uuid, today=last_week_date, closing_price=9764.0
    )

    test_session.add(fake_first_stage_analysis_last_week)
    test_session.commit()
    test_session.refresh(fake_first_stage_analysis_last_week)

    fake_first_stage_analysis_current_week = FirstStageAnalysisModel(
        uuid_analysis=fake_analysis.uuid, uuid_currency=fake_currency.uuid, today=today_date, closing_price=569.52
    )

    test_session.add(fake_first_stage_analysis_current_week)
    test_session.commit()
    test_session.refresh(fake_first_stage_analysis_current_week)

    sut = WeekPercentageValorizationService(
        session=test_session, closing_price_service=ClosingPriceService(session=test_session)
    )

    symbol = "BTC"
    week_percentage = Decimal(-94.17)

    # Act
    sut.update_last([{symbol: week_percentage}])

    # Assert
    updated_model = (
        test_session.query(FirstStageAnalysisModel)
        .filter_by(uuid_currency=fake_currency.uuid)
        .order_by(FirstStageAnalysisModel.today.desc())
        .first()
    )

    assert updated_model is not None
    assert updated_model.week_increase_percentage == pytest.approx(week_percentage)

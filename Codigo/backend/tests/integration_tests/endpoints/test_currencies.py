import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.dependencies.session import get_db
from src.api.routes.currencies import read_cryptos
from src.main import backend_app
from src.models.schemas.currency_info import CurrencyInfoResponse, LastUpdate


@pytest.mark.asyncio
async def test_return_currency_info_response_with_status_code_200(self, mocker):

    # Arrange
    db_mock = mocker.Mock()
    collector_mock = mocker.Mock()
    collector_mock.get_cryptos.return_value = CurrencyInfoResponse(
        last_update=LastUpdate(time=datetime.datetime.now(), data=[]),
        next_update=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    mocker.patch("src.api.routes.currencies.CurrenciesLogoCollector", return_value=collector_mock)

    backend_app.dependency_overrides[get_db] = db_mock
    client = TestClient(backend_app)
    # Act
    response = client.get("api/currency/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response, CurrencyInfoResponse)
    assert response.data == []

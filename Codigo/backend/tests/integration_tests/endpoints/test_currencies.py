import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import backend_app
from src.models.schemas.currency_info import CurrencyInfoResponse

client = TestClient(backend_app)


@pytest.mark.asyncio
async def test_raise_http_exception_when_no_cryptocurrencies_and_collection_fails(mocker):
    mocker.patch("src.repository.crud.currencies_info_schedule_repository.get_last_update", return_value=None)
    response = client.get("api/currency/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Nenhuma criptomoeda encontrada no banco de dados!"

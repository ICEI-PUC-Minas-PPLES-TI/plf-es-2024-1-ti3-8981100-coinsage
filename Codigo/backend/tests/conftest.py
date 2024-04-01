import os

import asgi_lifespan
import fastapi
import httpx
import pytest
from sqlalchemy import create_engine

from src.main import initialize_backend_application
from src.models.db.base import Base
from src.repository.database import SessionLocal


@pytest.fixture(name="backend_test_app")
def backend_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return initialize_backend_application()


@pytest.fixture(name="initialize_backend_test_application")
async def initialize_backend_test_application(backend_test_app: fastapi.FastAPI) -> fastapi.FastAPI:  # type: ignore
    async with asgi_lifespan.LifespanManager(backend_test_app):
        yield backend_test_app


@pytest.fixture(name="async_client")
async def async_client(initialize_backend_test_application: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with httpx.AsyncClient(
        app=initialize_backend_test_application,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


TEST_DB_PATH = "sqlite:///:memory:"
engine = create_engine(TEST_DB_PATH, connect_args={"check_same_thread": False})


@pytest.fixture(scope="session", name="db")
def db():
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)

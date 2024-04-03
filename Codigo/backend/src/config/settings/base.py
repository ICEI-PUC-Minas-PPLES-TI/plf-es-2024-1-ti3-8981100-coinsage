import logging
import pathlib

import decouple
import pydantic
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    TITLE: str = "CoinSage API"
    VERSION: str = "0.0.1"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    SERVER_HOST: str = decouple.config("SERVER_HOST", default="127.0.0.1", cast=str)  # type: ignore
    SERVER_PORT: int = decouple.config("SERVER_PORT", default=8000, cast=int)  # type: ignore
    SERVER_WORKERS: int = decouple.config("SERVER_WORKERS", default=4, cast=int)  # type: ignore
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    DATABASE_HOST: str = decouple.config("DATABASE_HOST", cast=str)  # type: ignore
    DATABASE_PORT: int = decouple.config("DATABASE_PORT", cast=int)  # type: ignore
    DATABASE_USER: str = decouple.config("DATABASE_USER", cast=str)  # type: ignore
    DATABASE_PASSWORD: str = decouple.config("DATABASE_PASSWORD", cast=str)  # type: ignore
    DATABASE_NAME: str = decouple.config("DATABASE_NAME", cast=str)  # type: ignore

    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", default=True, cast=bool)  # type: ignore
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://127.0.0.1:3000",  # React docker port
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    CMC_API_KEY: str = decouple.config("CMC_API_KEY", cast=str)  # type: ignore

    # ===== Schedules =====
    SCHEDULES: dict[str, dict[str, int]] = {
        "update_currencies_info": {
            "hour": 6,
            "minute": 0,
            "second": 0,
        },
        "get_all_analysis":{
            "hour": 8,
            "minute": 0,
            "second": 0,
        }
    }

    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }

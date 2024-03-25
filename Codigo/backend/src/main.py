import fastapi
import uvicorn
from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.api.endpoints import router as api_endpoint_router
from src.config.manager import settings
from src.models.db.base import Base
from src.repository.database import engine, SessionLocal
from src.schedules.update_currencies_info import start_schedules, stop_schdeules

Base.metadata.create_all(bind=engine)


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()


@backend_app.on_event("startup")
def schedules() -> None:
    with SessionLocal() as db:
        start_schedules(app_db=db)


@backend_app.on_event("shutdown")
def shutdown_event() -> None:
    stop_schdeules()


if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )

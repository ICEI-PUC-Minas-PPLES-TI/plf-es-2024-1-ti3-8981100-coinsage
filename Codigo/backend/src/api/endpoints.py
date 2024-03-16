import fastapi

from src.api.routes.edwin_method import router as edwin_method_router

router = fastapi.APIRouter()

router.include_router(router=edwin_method_router)

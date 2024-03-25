import fastapi

from src.api.routes.currencies import router as currencies_router
from src.api.routes.edwin_method import router as edwin_method_router
from src.api.routes.user import router as users_router

router = fastapi.APIRouter()

router.include_router(router=edwin_method_router)
router.include_router(router=currencies_router)

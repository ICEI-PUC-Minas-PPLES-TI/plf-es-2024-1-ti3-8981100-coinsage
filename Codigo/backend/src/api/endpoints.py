import fastapi

from src.api.controllers.analysis import router as edwin_method_router
from src.api.controllers.currencies import router as currencies_router
from src.api.controllers.workbook import router as workbook_router
from src.api.controllers.user import router as users_router
from src.api.controllers.wallet import router as wallet_router

router = fastapi.APIRouter()

router.include_router(router=edwin_method_router)
router.include_router(router=currencies_router)
router.include_router(router=workbook_router)
router.include_router(router=wallet_router)
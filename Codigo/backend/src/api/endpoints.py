from fastapi import APIRouter, Depends

from src.api.controllers.analysis import router as edwin_method_router
from src.api.controllers.auth import router as auth_router
from src.api.controllers.currencies import router as currencies_router
from src.api.controllers.wallet import router as wallet_router
from src.api.controllers.workbook import router as workbook_router
from src.security.authentication import get_current_user, oauth2_scheme

router = APIRouter()

router.include_router(router=edwin_method_router)
router.include_router(router=currencies_router)
router.include_router(router=workbook_router)
router.include_router(router=auth_router)
router.include_router(router=wallet_router, dependencies=[Depends(oauth2_scheme), Depends(get_current_user)])

import fastapi

router = fastapi.APIRouter(prefix="/edwin_method", tags=["edwin_method"])


@router.get(
    path="",
    name="edwin_method:read-last-analysis",
    response_model=str,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_accounts() -> str:
    return "Here is the last analysis"

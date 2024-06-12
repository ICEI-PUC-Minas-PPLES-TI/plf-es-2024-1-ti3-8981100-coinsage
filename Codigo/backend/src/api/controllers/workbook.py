import os
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.repository.crud.analysis_info_repository import get_last
from src.services.workbook.workbook_service import WorkbookService
from src.security.authentication import get_current_user
from src.models.schemas.user import UserResponse

router = APIRouter(prefix="/workbook", tags=["Workbook"])


@router.get(
    path="/",
    name="Workbook Analysis",
    response_class=FileResponse,
    description="Download de planilha com a análise completa",
    status_code=status.HTTP_200_OK,
)
async def generate_workbook(db: Session = Depends(get_db)):
    last_analysis = get_last(db)
    if not last_analysis:
        raise HTTPException(status_code=404, detail="No completed analysis found.")

    formatted_datetime = last_analysis.date.strftime("%d-%m-%Y às %H.%M")
    file_path = f"análise {formatted_datetime}.xlsx"
    filename = file_path

    headers = [
        "SETOR",
        "CRIPTOMOEDA",
        "RANKING",
        "VALOR MERCADO (US$ BILHÕES)",
        "DATA VALORIZ. SEMANAL > 10%",
        "VALORIZ. NESTA DATA (%)",
        "PREÇO NO MOMENTO (US$)",
        "PREÇO SEMANAL FECHAMENTO (US$)",
        "PREÇO SEMANAL ABERTURA (US$)",
        "EMA(8) SEMANAL",
        "PREÇO SEMANAL FECHAMENTO > EMA (8)",
        "EMA (8) > PREÇO SEMANAL ABERTURA",
        "MÉDIAS MÓVEIS DIÁRIAS ALINHADAS",
        "DATA AUMENTO DE VOLUME (d)",
        "AUMENTO DE VOLUME (w)",
        "AUMENTO DE VOLUME",
        "VOLUME ATUAL",
        "VOLUME ANTES DO AUMENTO",
        "VOLUME > 200%",
        "SINAL DE COMPRA"
    ]

    workbook_service = WorkbookService(db)
    workbook = workbook_service.create_workbook(headers)
    filled_workbook = workbook_service.fill_workbook(workbook, headers, str(last_analysis.uuid))
    styled_workbook = workbook_service.style_workbook(filled_workbook)
    formated_workbook = workbook_service.format_workbook(styled_workbook)

    # formated_workbook.save(file_path)
    file_stream = BytesIO()
    formated_workbook.save(file_stream)
    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

    # if os.path.exists(file_path):
    #     return FileResponse(
    #         path=file_path,
    #         filename=filename,
    #         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     )
    # else:
    #     raise HTTPException(status_code=404, detail="File not found.")
    
@router.get("/wallet", name="Workbook Wallet", response_class=StreamingResponse)
async def generate_wallet_workbook(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
):
    headers = ["CRIPTOMOEDA", "QUANTIDADE", "VALOR (US$)", "DATA", "PREÇO NA COMPRA (US$)"]
    workbook_service = WorkbookService(db)
    workbook = workbook_service.create_wallet_workbook(headers)
    filled_workbook = workbook_service.fill_wallet_workbook(workbook, headers, current_user.id)
    
    file_stream = BytesIO()
    filled_workbook.save(file_stream)
    file_stream.seek(0)
    filename = f"wallet_{current_user.id}.xlsx"

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
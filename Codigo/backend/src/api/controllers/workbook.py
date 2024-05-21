from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.api.dependencies.session import get_db
from src.services.workbook.workbook_service import WorkbookService
from src.repository.crud.analysis_info_repository import get_last
import os

router = APIRouter(
    prefix="/workbook",
    tags=["Workbook"]
)

@router.get(
    path="/", 
    name="Workbook Analysis",
    response_class=FileResponse,
    description="Download de planilha com a análise completa",
    status_code=status.HTTP_200_OK
)
async def generate_workbook(db: Session = Depends(get_db)):
    last_analysis = get_last(db)
    if not last_analysis:
        raise HTTPException(status_code=404, detail="No completed analysis found.")

    formatted_datetime = last_analysis.date.strftime("%d-%m-%Y às %H.%M")
    file_path = f"análise {formatted_datetime}.xlsx"
    filename = file_path

    headers = [
        #"CATEGORY",
        "SYMBOL",
        "RANKING",
        "MARKET CAP",
        "INCREASE DATE",
        "% WEEK INCREASE",
        "CLOSING PRICE",
        "LAST WEEK CLOSING PRICE"
        "OPEN PRICE",
        "EMA8",
        "WEEK CLOSING PRICE > EMA8(w)",
        "EMA8 > WEEK OPEN PRICE",
        "EMAs ALIGNED",
        "INCREASE VOLUME(d) DATE",
        "INCREASE VOLUME(w)",
        "INCREASE VOLUME",
        "TODAY VOLUME",
        "VOLUME BEFORE INCREASE",
        "% VOLUME/VOLUME DAY BEFORE",
        "VOLUME > 200%",
        "BUY SIGNAL",
        #"1 YEAR",
        #"180 DAYS",
        #"90 DAYS",
        #"30 DAYS",
        #"7 DAYS",
        #"APPRECIATION IS GREATER THAN BITCOIN"
    ]

    workbook_service = WorkbookService(db)
    workbook = workbook_service.create_workbook(headers)
    filled_workbook = workbook_service.fill_workbook(workbook, headers, str(last_analysis.uuid))

    filled_workbook.save(file_path)

    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        raise HTTPException(status_code=404, detail="File not found.")

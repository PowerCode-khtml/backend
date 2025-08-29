from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trend import StoreRankResponse
from app.schemas.base_response import GenericResponse
from app.crud import trend as trend_crud

router = APIRouter(prefix="/trend", tags=["trend"])

@router.get("/store", response_model=GenericResponse[StoreRankResponse])
def get_store_rankings_api(db: Session = Depends(get_db)):
    """
    인기 상점 순위 조회
    """
    rankings = trend_crud.get_store_rankings(db)
    return GenericResponse.success_response(data=StoreRankResponse(rankings=rankings))

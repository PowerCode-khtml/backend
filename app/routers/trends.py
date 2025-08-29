from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trend import StoreRankResponse, ProductRankResponse, EventRankResponse, SearchTrendResponse
from app.schemas.base_response import GenericResponse
from app.crud import trend as trend_crud

router = APIRouter(prefix="/trend", tags=["trend"])

@router.get("/", response_model=GenericResponse[SearchTrendResponse])
def get_search_rankings_api(db: Session = Depends(get_db)):
    """
    인기 검색어 순위 조회
    """
    rankings = trend_crud.get_search_trend_rankings(db)
    return GenericResponse.success_response(data=SearchTrendResponse(rankings=rankings))

@router.get("/store", response_model=GenericResponse[StoreRankResponse])
def get_store_rankings_api(db: Session = Depends(get_db)):
    """
    인기 상점 순위 조회
    """
    rankings = trend_crud.get_store_rankings(db)
    return GenericResponse.success_response(data=StoreRankResponse(rankings=rankings))

@router.get("/product", response_model=GenericResponse[ProductRankResponse])
def get_product_rankings_api(db: Session = Depends(get_db)):
    """
    인기 상품 순위 조회
    """
    rankings = trend_crud.get_product_rankings(db)
    return GenericResponse.success_response(data=ProductRankResponse(rankings=rankings))

@router.get("/event", response_model=GenericResponse[EventRankResponse])
def get_event_rankings_api(db: Session = Depends(get_db)):
    """
    인기 이벤트 순위 조회
    """
    rankings = trend_crud.get_event_rankings(db)
    return GenericResponse.success_response(data=EventRankResponse(rankings=rankings))

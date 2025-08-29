from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.market import MarketListResponse
from app.schemas.base_response import GenericResponse
from app.crud import market as market_crud

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/", response_model=GenericResponse[MarketListResponse])
def get_all_markets(db: Session = Depends(get_db)):
    """
    모든 마켓 목록 조회
    """
    markets = market_crud.get_markets(db)
    return GenericResponse.success_response(data=MarketListResponse(marketList=markets))

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.market import MarketListResponse, RecommendRequest, RecommendResponse
from app.schemas.base_response import GenericResponse
from app.crud import market as market_crud
from app.services import recommend

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/", response_model=GenericResponse[MarketListResponse])
def get_all_markets(db: Session = Depends(get_db)):
    """
    모든 마켓 목록 조회
    """
    markets = market_crud.get_markets(db)
    return GenericResponse.success_response(data=MarketListResponse(marketList=markets))

@router.post("/recommend", response_model=GenericResponse[RecommendResponse])
def recommend_market(request: RecommendRequest):
    """
    사용자 선호도에 따른 맞춤 시장 추천
    """
    # JSON 파일의 절대 경로
    json_path = "./data_all_cases.json"

    # recommend 서비스는 이제 자체적으로 DB 세션을 처리합니다.
    result = recommend.top1_from_file(
        q1_timeslot=request.q1,
        q2_vibe=request.q2,
        q3_transport=request.q3,
        q4_purposes=request.q4,
        json_path=json_path
    )

    if not result or not result.get("market"):
        return GenericResponse.error_response(
            error_message="추천 결과를 찾을 수 없습니다.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    response_data = RecommendResponse(
        top1Market=result["market"],
        marketAddress=result.get("address")
    )

    return GenericResponse.success_response(data=response_data)
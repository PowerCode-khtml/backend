import json
from typing import Iterable, Optional

from app.database import SessionLocal
from app.models.market import Market

def _canon_purposes(purposes: Iterable[str] | str) -> str:
    if isinstance(purposes, str):
        items = [x.strip() for x in purposes.split(',') if x.strip()]
    else:
        items = [str(x).strip() for x in purposes if str(x).strip()]
    return ','.join(sorted(items))

def _get_address_by_name(market_name: str) -> Optional[str]:
    """
    시장 이름으로 주소를 조회합니다.
    SQLAlchemy 세션을 사용하여 데이터베이스와 상호작용합니다.
    """
    if not market_name:
        return None

    db = SessionLocal()
    try:
        market = db.query(Market).filter(Market.marketName == market_name).first()
        return market.address if market else None
    finally:
        db.close()

def top1_from_file(
    q1_timeslot: str,   # '평일 낮' | '평일 저녁' | '주말 낮' | '주말 저녁'
    q2_vibe: str,       # '활기 선호' | '보통' | '한적 선호'
    q3_transport: str,  # '자차' | '자전거' | '도보' | '대중교통'
    q4_purposes: Iterable[str] | str,  # ['먹거리탐방','장보기'] 또는 '먹거리탐방,장보기'
    json_path: str = "data_all_cases.json"
) -> Optional[dict]:
    """
    사용자 입력과 JSON 데이터를 기반으로 최적의 시장을 추천하고 주소를 반환합니다.
    """
    key_q4 = _canon_purposes(q4_purposes)

    with open(json_path, "r", encoding="utf-8") as f:
        rows = json.load(f)

    for r in rows:
        if (
            r.get("Q1_시간대") == q1_timeslot and
            r.get("Q2_분위기") == q2_vibe and
            r.get("Q3_교통")  == q3_transport and
            _canon_purposes(r.get("Q4_체류목적", "")) == key_q4
        ):
            market = r.get("Top1_시장")
            # DB 조회를 위해 내부 함수 호출
            address = _get_address_by_name(market)
            return {"market": market, "address": address}

    return None
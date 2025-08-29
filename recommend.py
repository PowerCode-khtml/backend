import json
from typing import Iterable, Optional, Any

def _canon_purposes(purposes: Iterable[str] | str) -> str:
    if isinstance(purposes, str):
        items = [x.strip() for x in purposes.split(',') if x.strip()]
    else:
        items = [str(x).strip() for x in purposes if str(x).strip()]
    return ','.join(sorted(items))

def _get_address_by_name(db_conn: Any, market_name: str, placeholder: str | None = None) -> Optional[str]:

    if not market_name:
        return None

    # 플레이스홀더 자동 감지
    if placeholder is None:
        mod = (getattr(db_conn, "__module__", "") or getattr(db_conn.__class__, "__module__", "")).lower()
        placeholder = "?" if "sqlite3" in mod else "%s"

    sql = f"SELECT address FROM market WHERE marketName = {placeholder} LIMIT 1"
    cur = db_conn.cursor()
    try:
        cur.execute(sql, (market_name,))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        try:
            cur.close()
        except Exception:
            pass

def top1_from_file(
    q1_timeslot: str,   # '평일 낮' | '평일 저녁' | '주말 낮' | '주말 저녁'
    q2_vibe: str,       # '활기 선호' | '보통' | '한적 선호'
    q3_transport: str,  # '자차' | '자전거' | '도보' | '대중교통'
    q4_purposes: Iterable[str] | str,  # ['먹거리탐방','장보기'] 또는 '먹거리탐방,장보기'
    db_conn: Any,       # DB-API 커넥션 (주소 조회용)
    json_path: str = "data_all_cases.json",
    placeholder: str | None = None
) -> Optional[dict]:

    key_q4 = _canon_purposes(q4_purposes)

    with open(json_path, "r", encoding="utf-8") as f:
        rows = json.load(f)  # rows: List[dict]

    for r in rows:
        if (
            r.get("Q1_시간대") == q1_timeslot and
            r.get("Q2_분위기") == q2_vibe and
            r.get("Q3_교통")  == q3_transport and
            _canon_purposes(r.get("Q4_체류목적", "")) == key_q4
        ):
            market = r.get("Top1_시장")
            address = _get_address_by_name(db_conn, market, placeholder=placeholder)
            return {"market": market, "address": address}

    return None
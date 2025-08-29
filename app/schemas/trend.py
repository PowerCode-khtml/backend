from pydantic import BaseModel
from typing import List

class StoreRankInfo(BaseModel):
    rank: int
    storeName: str
    imgUrl: str | None

class StoreRankResponse(BaseModel):
    rankings: List[StoreRankInfo]

from pydantic import BaseModel
from typing import List

class StoreRankInfo(BaseModel):
    rank: int
    storeName: str
    imgUrl: str | None

class StoreRankResponse(BaseModel):
    rankings: List[StoreRankInfo]

class ProductRankInfo(BaseModel):
    rank: int
    mediaUrl: str | None
    productName: str
    like_count: int

class ProductRankResponse(BaseModel):
    rankings: List[ProductRankInfo]

class EventRankInfo(BaseModel):
    rank: int
    eventName: str
    imgUrl: str | None
    like_count: int

class EventRankResponse(BaseModel):
    rankings: List[EventRankInfo]

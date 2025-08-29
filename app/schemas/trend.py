from pydantic import BaseModel, Field
from typing import List

class StoreRankInfo(BaseModel):
    rank: int
    storeId: int
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

class SearchTrendInfo(BaseModel):
    rank: int
    searchName: str = Field(..., alias="keyword")

class SearchTrendResponse(BaseModel):
    rankings: List[SearchTrendInfo]

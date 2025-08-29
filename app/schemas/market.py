from pydantic import BaseModel, Field
from typing import List, Union

class MarketInfo(BaseModel):
    marketCode: int = Field(..., alias='marketid')
    marketName: str

    class Config:
        from_attributes = True
        populate_by_name = True

class MarketListResponse(BaseModel):
    marketList: List[MarketInfo]


class RecommendRequest(BaseModel):
    q1: str
    q2: str
    q3: str
    q4: Union[str, List[str]]


class RecommendResponse(BaseModel):
    top1Market: str
    marketAddress: str | None = None

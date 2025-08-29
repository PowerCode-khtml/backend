from pydantic import BaseModel, Field
from typing import List

class MarketInfo(BaseModel):
    marketCode: int = Field(..., alias='marketid')
    marketName: str

    class Config:
        from_attributes = True
        populate_by_name = True

class MarketListResponse(BaseModel):
    marketList: List[MarketInfo]

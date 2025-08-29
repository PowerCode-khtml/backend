from pydantic import BaseModel, Field
from typing import List, Optional

class KeywordItem(BaseModel):
    keyword: str

class KeywordListDto(BaseModel):
    keywordList: List[KeywordItem]

class KeywordResponse(BaseModel):
    responseDto: KeywordListDto
    error: Optional[str] = None
    success: bool = True


class MarketInfoByKeyword(BaseModel):
    marketName: str
    description: str

"""
리뷰 스키마
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 리뷰 기본 스키마
class ReviewBase(BaseModel):
    score: float = Field(..., ge=0, le=5) # 0~5점
    content: str
    imgUrl: Optional[str] = None

# 리뷰 생성 스키마
class ReviewCreate(ReviewBase):
    pass

# 리뷰 응답 스키마
class ReviewResponse(ReviewBase):
    reviewid: int
    feedid: int
    userid: int
    createdAt: datetime

    class Config:
        from_attributes = True

# API 수정을 위한 새로운 스키마
class ReviewInfo(BaseModel):
    content: str = Field(..., serialization_alias="reviewContent")
    imgUrl: Optional[str] = Field(None, serialization_alias="reviewImageUrl")
    rating: float = Field(..., serialization_alias="reviewScore")
    created_at: datetime = Field(..., serialization_alias="createAt")

    class Config:
        from_attributes = True

class ReviewListResponse(BaseModel):
    avgScore: float
    reviewList: List[ReviewInfo]

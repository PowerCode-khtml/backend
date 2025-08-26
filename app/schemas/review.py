"""
리뷰 스키마
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    content: str
    imgUrl: Optional[str] = None
    rating: int  # 1-5

class ReviewCreate(ReviewBase):
    feedid: int
    userid: int

class ReviewResponse(ReviewBase):
    reviewid: int
    userid: int
    feedid: int
    created_at: datetime
    
    class Config:
        from_attributes = True

"""
비디오 스키마
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class VideoInfo(BaseModel):
    videoId: int = Field(..., alias="videoId")
    storeId: int = Field(..., alias="storeId")
    videoName: str = Field(..., alias="videoName")
    videoUrl: str = Field(..., alias="videoUrl")
    createdAt: datetime = Field(..., alias="createdAt")
    videoContent: Optional[str] = Field(None, alias="videoContent")
    storeImage: Optional[str] = Field(None, alias="storeImage")
    videoLikeCount: int = Field(..., alias="videoLikeCount")
    videoReviewCount: int = Field(..., alias="videoReviewCount")

    class Config:
        from_attributes = True
        populate_by_name = True

class VideoListResponse(BaseModel):
    videoList: List[VideoInfo]

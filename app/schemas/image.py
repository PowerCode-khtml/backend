"""
이미지 생성 스키마 (해커톤 AI 기능)
"""
from pydantic import BaseModel
from typing import Optional

class FeedMediaResponseData(BaseModel):
    feedMediaUrl: Optional[str] = None
    feedBody: Optional[str] = None

class GeneratedFeedMediaResponse(BaseModel):
    responseDto: FeedMediaResponseData
    error: Optional[str] = None
    success: bool
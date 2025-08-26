"""
이미지 생성 스키마 (해커톤 AI 기능)
"""
from pydantic import BaseModel
from typing import Optional

class ImageGenerationRequest(BaseModel):
    """AI 이미지 생성 요청"""
    storeid: int
    promoKind: str  # "store", "product", "event"
    prompt: Optional[str] = None
    # 상품 피드용 추가 정보
    productName: Optional[str] = None
    productDescription: Optional[str] = None
    # 이벤트 피드용 추가 정보  
    eventName: Optional[str] = None
    eventDescription: Optional[str] = None

class ImageGenerationResponse(BaseModel):
    """AI 이미지 생성 응답"""
    success: bool
    message: str
    feedid: Optional[int] = None
    mediaUrl: Optional[str] = None
    prompt_used: Optional[str] = None
    error: Optional[str] = None

class QuickPosterRequest(BaseModel):
    """빠른 포스터 생성 (상점 정보 기반)"""
    storeid: int
    message: str = "새로운 소식이 있어요!"
    style: Optional[str] = "modern"  # modern, vintage, cute 등

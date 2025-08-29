"""
피드 스키마 (통합 피드 시스템)
"""
from pydantic import BaseModel, Field
from typing import Optional, Union, List
from datetime import datetime
from enum import Enum

class PromoKindEnum(str, Enum):
    store = "store"
    product = "product"
    event = "event"

class MediaTypeEnum(str, Enum):
    image = "image"
    video = "video"

class FeedBase(BaseModel):
    promoKind: PromoKindEnum
    mediaType: MediaTypeEnum
    prompt: Optional[str] = None  # AI 이미지 생성용
    mediaUrl: str
    body: Optional[str] = None

class FeedCreate(FeedBase):
    storeid: int

class FeedResponse(FeedBase):
    feedid: int
    storeid: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 상점 피드 전용
class StoreFeedCreate(BaseModel):
    feedid: int
    description: Optional[str] = None
    imgUrl: str

class StoreFeedResponse(BaseModel):
    feedid: int
    description: Optional[str] = None
    imgUrl: str
    
    class Config:
        from_attributes = True

# 상품 피드 전용  
class ProductFeedCreate(BaseModel):
    feedid: int
    productName: str
    description: str
    imgUrl: str
    productCategoryID: int

class ProductFeedResponse(BaseModel):
    feedid: int
    productName: str
    description: str
    imgUrl: str
    productCategoryID: int
    
    class Config:
        from_attributes = True

# 이벤트 피드 전용
class EventFeedCreate(BaseModel):
    feedid: int
    eventName: str
    description: str
    imgUrl: str
    start_at: datetime
    end_at: datetime

class EventFeedResponse(BaseModel):
    feedid: int
    eventName: str
    description: str
    imgUrl: str
    start_at: datetime
    end_at: datetime
    
    class Config:
        from_attributes = True


# AI 이미지 생성 응답 스키마
class FeedMediaResponseData(BaseModel):
    feedMediaUrl: str
    feedBody: str

class GeneratedFeedMediaResponse(BaseModel):
    responseDto: FeedMediaResponseData
    success: bool = True
    error: Optional[str] = None

# 새로운 피드 상세 정보 스키마
class FeedInfo(BaseModel):
    feedId: int = Field(..., serialization_alias="feedId")
    storeId: int = Field(..., serialization_alias="storeId")
    storeName: str = Field(..., serialization_alias="storeName")
    storeImageUrl: Optional[str] = Field(None, serialization_alias="storeImageUrl")
    createdAt: datetime = Field(..., serialization_alias="createdAt")
    feedTitle: str = Field(..., serialization_alias="feedTitle") # Derived from feedContent
    feedContent: str = Field(..., serialization_alias="feedContent")
    feedImageUrl: str = Field(..., serialization_alias="feedImageUrl")
    feedType: str = Field(..., serialization_alias="feedType")
    feedLikeCount: int = Field(..., serialization_alias="feedLikeCount")
    feedReviewCount: int = Field(..., serialization_alias="feedReviewCount")
    isLiked: bool = Field(..., serialization_alias="isLiked")

    class Config:
        from_attributes = True

# 새로운 피드 목록 응답 스키마
class FeedListResponse(BaseModel):
    feedList: List[FeedInfo]

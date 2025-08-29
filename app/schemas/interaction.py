"""
상호작용 스키마 (좋아요, 구독)
"""
from pydantic import BaseModel, Field

# 피드 좋아요
class FeedLikeCreate(BaseModel):
    userid: int
    feedid: int

class FeedLikeResponse(BaseModel):
    userid: int
    feedid: int
    
    class Config:
        from_attributes = True

class FeedLikeToggleResponse(BaseModel):
    is_liked: bool = Field(..., alias="isLiked")
    likes_count: int = Field(..., alias="likesCount")

    class Config:
        from_attributes = True
        populate_by_name = True

class FeedLikesCountResponse(BaseModel):
    feed_id: int
    likes_count: int

# 구독
class SubscriptionCreate(BaseModel):
    userid: int
    storeid: int

class SubscriptionResponse(BaseModel):
    userid: int
    storeid: int
    
    class Config:
        from_attributes = True

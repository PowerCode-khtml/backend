"""
상호작용 스키마 (좋아요, 구독)
"""
from pydantic import BaseModel

# 피드 좋아요
class FeedLikeCreate(BaseModel):
    userid: int
    feedid: int

class FeedLikeResponse(BaseModel):
    userid: int
    feedid: int
    
    class Config:
        from_attributes = True

# 구독
class SubscriptionCreate(BaseModel):
    userid: int
    storeid: int

class SubscriptionResponse(BaseModel):
    userid: int
    storeid: int
    
    class Config:
        from_attributes = True

"""
상점 스키마
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import time

class StoreBase(BaseModel):
    storeName: str
    tel: Optional[str] = None
    dayOpenTime: Optional[time] = None
    dayCloseTime: Optional[time] = None
    weekendOpenTime: Optional[time] = None
    weekendCloseTime: Optional[time] = None
    address: Optional[str] = None
    description: Optional[str] = None

class StoreCreate(StoreBase):
    marketid: int
    categoryid: int
    hostid: int

class StoreUpdate(BaseModel):
    storeName: Optional[str] = None
    tel: Optional[str] = None
    dayOpenTime: Optional[time] = None
    dayCloseTime: Optional[time] = None
    weekendOpenTime: Optional[time] = None
    weekendCloseTime: Optional[time] = None
    address: Optional[str] = None
    description: Optional[str] = None

class StoreResponse(StoreBase):
    storeid: int
    marketid: int
    categoryid: int
    hostid: int
    
    class Config:
        from_attributes = True


class StoreInDB(StoreResponse):
    pass

class StoreProfileFeed(BaseModel):
    mediaUrl: Optional[str] = None
    feedName: str
    like_count: int
    feedType: str

class StoreProfileResponse(BaseModel):
    storeImg: Optional[str] = None
    followerCount: int
    totalLikedCount: int
    isMyStore: bool
    storeDescript: Optional[str] = None
    storeAddress: Optional[str] = None
    storePhoneNumber: Optional[str] = None
    weekdayStart: Optional[str] = None
    weekdayEnd: Optional[str] = None
    weekendStart: Optional[str] = None
    weekendEnd: Optional[str] = None
    feeds: List[StoreProfileFeed]

class UserSubscriptionCreate(BaseModel):
    userId: int

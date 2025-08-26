"""
상점 스키마
"""
from pydantic import BaseModel
from typing import Optional
from datetime import time

class StoreBase(BaseModel):
    storeName: str
    tel: Optional[str] = None
    dayOpenTime: Optional[time] = None
    dayCloseTime: Optional[time] = None
    weekendOpenTime: Optional[time] = None
    weekendCloseTime: Optional[time] = None
    address: Optional[str] = None
    description: str

class StoreCreate(StoreBase):
    marketid: int
    categoryid: int
    hostID: int

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
    hostID: int
    
    class Config:
        from_attributes = True

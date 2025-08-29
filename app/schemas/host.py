"""
호스트 스키마
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class HostBase(BaseModel):
    email: EmailStr
    name: str

class HostCreate(HostBase):
    password: str

class HostLogin(BaseModel):
    email: EmailStr
    password: str

class HostResponse(HostBase):
    hostid: int
    created_at: datetime
    
    class Config:
        from_attributes = True

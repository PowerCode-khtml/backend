"""
인증 스키마 (해커톤용 단순화)
"""
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    accessToken: str
    tokenType: str
    userType: str  # "user" or "host"
    userId: int

class TokenData(BaseModel):
    email: Optional[str] = None
    userType: Optional[str] = None
    userId: Optional[int] = None

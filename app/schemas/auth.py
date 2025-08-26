"""
인증 스키마 (해커톤용 단순화)
"""
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str  # "user" or "host"
    user_id: int

class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[str] = None
    user_id: Optional[int] = None

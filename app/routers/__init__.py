"""
API 라우터들 (해커톤용)
"""
from .auth import router as auth_router
from .feeds import router as feeds_router  
from .stores import router as stores_router
from .users import router as users_router
from .markets import router as markets_router
from .trends import router as trends_router

__all__ = ["auth_router", "feeds_router", "stores_router", "users_router", "markets_router", "trends_router"]

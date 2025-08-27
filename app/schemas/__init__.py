"""
API 스키마들 (해커톤용)
"""
from .user import UserCreate, UserResponse, UserLogin, UserUpdate
from .host import HostCreate, HostResponse, HostLogin
from .store import StoreCreate, StoreResponse, StoreUpdate
from .feed import (
    FeedCreate, FeedResponse, 
    StoreFeedCreate, StoreFeedResponse,
    ProductFeedCreate, ProductFeedResponse,
    EventFeedCreate, EventFeedResponse
)
from .review import ReviewCreate, ReviewResponse
from .interaction import FeedLikeCreate, FeedLikeResponse, SubscriptionCreate, SubscriptionResponse
from .image import GeneratedFeedMediaResponse
from .category import (
    StoreCategoryCreate, StoreCategoryResponse,
    ProductCategoryCreate, ProductCategoryResponse,
    MarketCreate, MarketResponse
)
from .auth import Token, TokenData
from .payment import PaymentMethodCreate, PaymentMethodResponse
from .base_response import GenericResponse

__all__ = [
    # User & Host
    "UserCreate", "UserResponse", "UserLogin", "UserUpdate",
    "HostCreate", "HostResponse", "HostLogin",
    
    # Store
    "StoreCreate", "StoreResponse", "StoreUpdate",
    
    # Feed System (핵심)
    "FeedCreate", "FeedResponse",
    "StoreFeedCreate", "StoreFeedResponse", 
    "ProductFeedCreate", "ProductFeedResponse",
    "EventFeedCreate", "EventFeedResponse",
    
    # Review & Interaction
    "ReviewCreate", "ReviewResponse",
    "FeedLikeCreate", "FeedLikeResponse",
    "SubscriptionCreate", "SubscriptionResponse",
    
    # AI Image Generation (특별 기능)
    "GeneratedFeedMediaResponse",
    
    # Categories
    "StoreCategoryCreate", "StoreCategoryResponse",
    "ProductCategoryCreate", "ProductCategoryResponse", 
    "MarketCreate", "MarketResponse",
    
    # Auth
    "Token", "TokenData",

    # Payment
    "PaymentMethodCreate", "PaymentMethodResponse",

    # Base Response
    "GenericResponse"
]
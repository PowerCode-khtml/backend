"""
피드 및 AI 이미지 생성 라우터
"""
from fastapi import (
    APIRouter, Depends, HTTPException, status, Query, 
    File, UploadFile, Form
)
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.feed import FeedCreate, FeedResponse
from app.schemas.review import ReviewCreate, ReviewResponse
from app.schemas.interaction import FeedLikeCreate
from app.schemas.image import GeneratedFeedMediaResponse, FeedMediaResponseData
from app.crud import feed as feed_crud, review as review_crud, store as store_crud
from app.services.image_generator import ImageGeneratorService

router = APIRouter(prefix="/feed", tags=["feeds"])

# --- 기존 피드 기능 ---

@router.get("/{market_id}", response_model=List[FeedResponse])
def get_feeds_by_market(
    market_id: int,
    skip: int = 0, 
    limit: int = 50,
    promo_kind: str = Query(None, description="피드 타입: store, product, event"),
    db: Session = Depends(get_db)
):
    """특정 시장의 피드 목록 조회"""
    return feed_crud.get_feeds_by_market(db, market_id=market_id, promo_kind=promo_kind, skip=skip, limit=limit)

@router.get("/{feed_id}", response_model=FeedResponse)
def get_feed(feed_id: int, db: Session = Depends(get_db)):
    """특정 피드 상세 조회"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail="피드를 찾을 수 없습니다")
    return feed

@router.get("/stores/{store_id}", response_model=List[FeedResponse])
def get_feeds_by_store(
    store_id: int, 
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """특정 상점의 피드 목록"""
    return feed_crud.get_feeds_by_store(db, store_id=store_id, skip=skip, limit=limit)

@router.post("/", response_model=FeedResponse)
def create_feed(feed: FeedCreate, db: Session = Depends(get_db)):
    """새 피드 생성"""
    return feed_crud.create_feed(db=db, feed=feed)

@router.post("/{feed_id}/like")
def toggle_feed_like(
    feed_id: int,
    user_id: int,  # 해커톤용 단순화 (실제로는 JWT에서 추출)
    db: Session = Depends(get_db)
):
    """피드 좋아요/좋아요 취소"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="피드를 찾을 수 없습니다")
    
    is_liked = feed_crud.toggle_feed_like(db, user_id=user_id, feed_id=feed_id)
    likes_count = feed_crud.get_feed_likes_count(db, feed_id=feed_id)
    
    return {
        "success": True,
        "is_liked": is_liked,
        "likes_count": likes_count
    }

@router.get("/{feed_id}/likes")
def get_feed_likes(feed_id: int, db: Session = Depends(get_db)):
    """피드 좋아요 수 조회"""
    likes_count = feed_crud.get_feed_likes_count(db, feed_id=feed_id)
    return {"feed_id": feed_id, "likes_count": likes_count}

@router.post("/{feed_id}/reviews", response_model=ReviewResponse)
def create_feed_review(
    feed_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """피드에 리뷰 작성"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="피드를 찾을 수 없습니다")
    
    review.feedid = feed_id
    return review_crud.create_review(db=db, review=review)

@router.get("/{feed_id}/reviews", response_model=List[ReviewResponse])
def get_feed_reviews(
    feed_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """피드의 리뷰 목록 조회"""
    return review_crud.get_reviews_by_feed(db, feed_id=feed_id, skip=skip, limit=limit)

# --- AI 이미지 생성 기능 ---

image_service = ImageGeneratorService()

@router.post("/generate", response_model=GeneratedFeedMediaResponse, tags=["ai-images"])
async def generate_feed_media(
    db: Session = Depends(get_db),
    feedType: str = Form(...),
    mediaType: str = Form(...),
    storeId: Optional[int] = Form(None),
    storeDescription: Optional[str] = Form(None),
    productName: Optional[str] = Form(None),
    categoryId: Optional[int] = Form(None),
    productDescription: Optional[str] = Form(None),
    eventName: Optional[str] = Form(None),
    eventDescription: Optional[str] = Form(None),
    eventStartAt: Optional[str] = Form(None),
    eventEndAt: Optional[str] = Form(None),
    storeImage: Optional[UploadFile] = File(None),
    productImage: Optional[UploadFile] = File(None),
    eventImage: Optional[UploadFile] = File(None)
):
    """피드 타입에 따라 프롬프트를 생성하고 AI 이미지를 생성합니다."""
    prompt = ""
    body_text = ""
    input_image: Optional[UploadFile] = None

    return GeneratedFeedMediaResponse(
        responseDto=FeedMediaResponseData(
            feedMediaUrl="https://marketcloud-bucket.s3.ap-northeast-2.amazonaws.com/generate/image/output.png",
            feedBody="더미 텍스트"
        ),
        success=True
    )

    # if mediaType == "video":
    #     return GeneratedFeedMediaResponse(
    #         responseDto=FeedMediaResponseData(),
    #         error="비디오 생성은 현재 지원되지 않습니다.",
    #         success=False
    #     )

    # if feedType == "store":
    #     if not all([storeId, storeDescription, storeImage]):
    #         raise HTTPException(status_code=400, detail="'store' 타입에 필요한 필드가 누락되었습니다.")
    #     store = store_crud.get_store(db, store_id=storeId)
    #     if not store:
    #         raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다.")
    #     prompt = image_service.create_store_prompt(store.storeName, storeDescription)
    #     body_text = storeDescription
    #     input_image = storeImage

    # elif feedType == "product":
    #     if not all([storeId, productName, categoryId, productDescription, productImage]):
    #         raise HTTPException(status_code=400, detail="'product' 타입에 필요한 필드가 누락되었습니다.")
    #     store = store_crud.get_store(db, store_id=storeId)
    #     if not store:
    #         raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다.")
    #     prompt = image_service.create_product_prompt(productName, productDescription, store.storeName)
    #     body_text = f"{{productName}}: {{productDescription}}"
    #     input_image = productImage

    # elif feedType == "event":
    #     if not all([eventName, eventDescription, eventStartAt, eventEndAt, eventImage]):
    #         raise HTTPException(status_code=400, detail="'event' 타입에 필요한 필드가 누락되었습니다.")
    #     prompt = image_service.create_event_prompt(eventName, eventDescription)
    #     body_text = f"{{eventName}}: {{eventDescription}}"
    #     input_image = eventImage

    # else:
    #     raise HTTPException(status_code=400, detail="잘못된 'feedType'입니다.")

    # if input_image:
    #     await image_service.save_uploaded_file(input_image)

    # generation_result = await image_service.generate_image(prompt)

    # if not generation_result["success"]:
    #     return GeneratedFeedMediaResponse(
    #         responseDto=FeedMediaResponseData(),
    #         error=generation_result.get("error", "이미지 생성에 실패했습니다."),
    #         success=False
    #     )

    # return GeneratedFeedMediaResponse(
    #     responseDto=FeedMediaResponseData(
    #         feedMediaUrl=generation_result["mediaUrl"],
    #         feedBody=body_text
    #     ),
    #     success=True
    # )

@router.post("/generate-dev", response_model=GeneratedFeedMediaResponse, tags=["ai-images"])
async def generate_feed_media(
    db: Session = Depends(get_db),
    feedType: str = Form(...),
    mediaType: str = Form(...),
    storeId: Optional[int] = Form(None),
    storeDescription: Optional[str] = Form(None),
    productName: Optional[str] = Form(None),
    categoryId: Optional[int] = Form(None),
    productDescription: Optional[str] = Form(None),
    eventName: Optional[str] = Form(None),
    eventDescription: Optional[str] = Form(None),
    eventStartAt: Optional[str] = Form(None),
    eventEndAt: Optional[str] = Form(None),
    storeImage: Optional[UploadFile] = File(None),
    productImage: Optional[UploadFile] = File(None),
    eventImage: Optional[UploadFile] = File(None)
):
    """피드 타입에 따라 프롬프트를 생성하고 AI 이미지를 생성합니다."""
    prompt = ""
    body_text = ""
    input_image: Optional[UploadFile] = None

    if mediaType == "video":
        return GeneratedFeedMediaResponse(
            responseDto=FeedMediaResponseData(),
            error="비디오 생성은 현재 지원되지 않습니다.",
            success=False
        )

    if feedType == "store":
        if not all([storeId, storeDescription, storeImage]):
            raise HTTPException(status_code=400, detail="'store' 타입에 필요한 필드가 누락되었습니다.")
        store = store_crud.get_store(db, store_id=storeId)
        if not store:
            raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다.")
        prompt = image_service.create_store_prompt(store.storeName, storeDescription)
        body_text = storeDescription
        input_image = storeImage

    elif feedType == "product":
        if not all([storeId, productName, categoryId, productDescription, productImage]):
            raise HTTPException(status_code=400, detail="'product' 타입에 필요한 필드가 누락되었습니다.")
        store = store_crud.get_store(db, store_id=storeId)
        if not store:
            raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다.")
        prompt = image_service.create_product_prompt(productName, productDescription, store.storeName)
        body_text = f"{{productName}}: {{productDescription}}"
        input_image = productImage

    elif feedType == "event":
        if not all([eventName, eventDescription, eventStartAt, eventEndAt, eventImage]):
            raise HTTPException(status_code=400, detail="'event' 타입에 필요한 필드가 누락되었습니다.")
        prompt = image_service.create_event_prompt(eventName, eventDescription)
        body_text = f"{{eventName}}: {{eventDescription}}"
        input_image = eventImage

    else:
        raise HTTPException(status_code=400, detail="잘못된 'feedType'입니다.")

    if input_image:
        await image_service.save_uploaded_file(input_image)

    generation_result = await image_service.generate_image(prompt)

    if not generation_result["success"]:
        return GeneratedFeedMediaResponse(
            responseDto=FeedMediaResponseData(),
            error=generation_result.get("error", "이미지 생성에 실패했습니다."),
            success=False
        )

    return GeneratedFeedMediaResponse(
        responseDto=FeedMediaResponseData(
            feedMediaUrl=generation_result["mediaUrl"],
            feedBody=body_text
        ),
        success=True
    )
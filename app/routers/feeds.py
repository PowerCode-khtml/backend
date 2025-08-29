"""
피드 및 AI 이미지 생성 라우터
"""
from fastapi import (
    APIRouter, Depends, HTTPException, status, Query, 
    File, UploadFile, Form
)
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime

from app.database import get_db
from app.schemas.feed import FeedCreate, FeedResponse, FeedInfo, FeedListResponse
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewListResponse
from app.schemas.interaction import FeedLikeCreate, FeedLikeToggleResponse, FeedLikesCountResponse
from app.schemas.image import GeneratedFeedMediaResponse, FeedMediaResponseData
from app.schemas.base_response import GenericResponse
from app.crud import feed as feed_crud, review as review_crud, store as store_crud
from app.services.image_generator import ImageGeneratorService
from app.services.s3 import S3Service

router = APIRouter(prefix="/feed", tags=["feeds"])

s3_service = S3Service()

# --- 피드 기능 ---

@router.post("/local", response_model=GenericResponse[FeedResponse])
def create_feed_local(
    db: Session = Depends(get_db),
    feedType: str = Form(...),
    mediaType: str = Form(...),
    hostId: int = Form(...),
    feedMediaFile: UploadFile = File(None),
    feedBody: str = Form(...),
    # Store-specific
    storeDescription: Optional[str] = Form(None),
    storeImage: Optional[UploadFile] = File(None),
    # Product-specific
    productName: Optional[str] = Form(None),
    categoryId: Optional[int] = Form(None),
    productDescription: Optional[str] = Form(None),
    productImage: Optional[UploadFile] = File(None),
    # Event-specific
    eventName: Optional[str] = Form(None),
    eventDescription: Optional[str] = Form(None),
    eventStartAt: Optional[datetime.datetime] = Form(None),
    eventEndAt: Optional[datetime.datetime] = Form(None),
    eventImage: Optional[UploadFile] = File(None),
):
    """새로운 피드를 유형에 따라 생성합니다 (S3 업로드 포함)."""
    # S3에 피드 미디어 파일 업로드
    feed_media_url = s3_service.upload_file(feedMediaFile)
    if not feed_media_url:
        return GenericResponse.error_response(
            error_message="S3에 피드 미디어를 업로드하지 못했습니다.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # TODO: 각 타입별 이미지들도 S3에 업로드 (현재는 로컬 경로 사용)
    store_image_url = ""
    product_image_url = ""
    event_image_url = ""

    stores = store_crud.get_stores_by_host(db, host_id=hostId)
    if not stores:
        return GenericResponse.error_response(
            error_message="상점을 찾을 수 없습니다.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    storeId = stores[0].storeid

    if storeImage:
        store_image_url = feed_media_url#s3_service.upload_file(storeImage)
    if productImage:
        product_image_url = feed_media_url#3_service.upload_file(productImage)
    if eventImage:
        event_image_url = feed_media_url#s3_service.upload_file(eventImage)

    # feedType에 따라 필수 파라미터 검증
    if feedType == "store":
        if not all([storeDescription, storeImage]):
            return GenericResponse.error_response(
                error_message="'store' 타입에 필요한 필드가 누락되었습니다: storeDescription, storeImage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    elif feedType == "product":
        if not all([productName, categoryId, productDescription, productImage]):
            return GenericResponse.error_response(
                error_message="'product' 타입에 필요한 필드가 누락되었습니다: productName, categoryId, productDescription, productImage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    elif feedType == "event":
        if not all([eventName, eventDescription, eventStartAt, eventEndAt, eventImage]):
            return GenericResponse.error_response(
                error_message="'event' 타입에 필요한 필드가 누락되었습니다: eventName, eventDescription, eventStartAt, eventEndAt, eventImage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    else:
        return GenericResponse.error_response(
            error_message="잘못된 'feedType'입니다. 'store', 'product', 'event' 중 하나여야 합니다.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    db_feed = feed_crud.create_feed_with_details(
        db=db,
        feed_type=feedType,
        media_type=mediaType,
        store_id=storeId,
        feed_body=feedBody,
        feed_media_url=feed_media_url,
        store_description=storeDescription,
        store_image_url=store_image_url,
        product_name=productName,
        category_id=categoryId,
        product_description=productDescription,
        product_image_url=product_image_url,
        event_name=eventName,
        event_description=eventDescription,
        event_start_at=eventStartAt,
        event_end_at=eventEndAt,
        event_image_url=event_image_url,
    )
    
    return GenericResponse.success_response(db_feed)

@router.post("/", response_model=GenericResponse[FeedResponse])
def create_feed(
    db: Session = Depends(get_db),
    feedType: str = Form(...),
    mediaType: str = Form(...),
    hostId: int = Form(...),
    feedMediaUrl: str = Form(...),
    feedBody: str = Form(...),
    # Store-specific
    storeDescription: Optional[str] = Form(None),
    storeImage: Optional[UploadFile] = File(None),
    # Product-specific
    productName: Optional[str] = Form(None),
    categoryId: Optional[int] = Form(None),
    productDescription: Optional[str] = Form(None),
    productImage: Optional[UploadFile] = File(None),
    # Event-specific
    eventName: Optional[str] = Form(None),
    eventDescription: Optional[str] = Form(None),
    eventStartAt: Optional[datetime.datetime] = Form(None),
    eventEndAt: Optional[datetime.datetime] = Form(None),
    eventImage: Optional[UploadFile] = File(None),
):
    """새로운 피드를 유형에 따라 생성합니다."""
    # TODO: 파일 처리 로직 추가 (S3 업로드 등)
    store_image_url = ""
    product_image_url = ""
    event_image_url = ""

    stores = store_crud.get_stores_by_host(db, host_id=hostId)
    if not stores:
        return GenericResponse.error_response(
            error_message="상점을 찾을 수 없습니다.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    storeId = stores[0].storeid

    if storeImage:
        # 예시: store_image_url = await save_file(storeImage)
        store_image_url = f"/uploads/{storeImage.filename}"
    if productImage:
        product_image_url = f"/uploads/{productImage.filename}"
    if eventImage:
        event_image_url = f"/uploads/{eventImage.filename}"

    # feedType에 따라 필수 파라미터 검증
    if feedType == "store":
        if not all([storeDescription, storeImage]):
            return GenericResponse.error_response(
                error_message="'store' 타입에 필요한 필드가 누락되었습니다: storeDescription, storeImage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    elif feedType == "product":
        if not all([productName, categoryId, productDescription, productImage]):
            return GenericResponse.error_response(
                error_message="'product' 타입에 필요한 필드가 누락되었습니다: productName, categoryId, productDescription, productImage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    elif feedType == "event":
        if not all([eventName, eventDescription, eventStartAt, eventEndAt, eventImage]):
            return GenericResponse.error_response(
                error_message="'event' 타입에 필요한 필드가 누락되었습니다: eventName, eventDescription, eventStartAt, eventEndAt, eventImage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    else:
        return GenericResponse.error_response(
            error_message="잘못된 'feedType'입니다. 'store', 'product', 'event' 중 하나여야 합니다.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    db_feed = feed_crud.create_feed_with_details(
        db=db,
        feed_type=feedType,
        media_type=mediaType,
        store_id=storeId,
        feed_body=feedBody,
        feed_media_url=feedMediaUrl,
        store_description=storeDescription,
        store_image_url=store_image_url,
        product_name=productName,
        category_id=categoryId,
        product_description=productDescription,
        product_image_url=product_image_url,
        event_name=eventName,
        event_description=eventDescription,
        event_start_at=eventStartAt,
        event_end_at=eventEndAt,
        event_image_url=event_image_url,
    )
    
    return GenericResponse.success_response(db_feed)

@router.get("/stores/{store_id}", response_model=GenericResponse[List[FeedResponse]])
def get_feeds_by_store(
    store_id: int, 
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """특정 상점의 피드 목록"""
    feeds = feed_crud.get_feeds_by_store(db, store_id=store_id, skip=skip, limit=limit)
    return GenericResponse.success_response(feeds)

@router.post("/{feed_id}/like", response_model=GenericResponse[FeedLikeToggleResponse])
def toggle_feed_like(
    feed_id: int,
    userId: int = Form(..., alias="userId"),
    db: Session = Depends(get_db)
):
    """피드 좋아요/좋아요 취소"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if not feed:
        return GenericResponse.error_response(
            error_message="피드를 찾을 수 없습니다",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    is_liked = feed_crud.toggle_feed_like(db, user_id=userId, feed_id=feed_id)
    likes_count = feed_crud.get_feed_likes_count(db, feed_id=feed_id)
    
    return GenericResponse.success_response(
        FeedLikeToggleResponse(is_liked=is_liked, likes_count=likes_count)
    )

@router.get("/{feed_id}/likes", response_model=GenericResponse[FeedLikesCountResponse])
def get_feed_likes(feed_id: int, db: Session = Depends(get_db)):
    """피드 좋아요 수 조회"""
    likes_count = feed_crud.get_feed_likes_count(db, feed_id=feed_id)
    return GenericResponse.success_response(
        FeedLikesCountResponse(feed_id=feed_id, likes_count=likes_count)
    )

@router.post("/{feed_id}/reviews", response_model=GenericResponse[ReviewResponse])
def create_feed_review(
    feed_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """피드에 리뷰 작성"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if not feed:
        return GenericResponse.error_response(
            error_message="피드를 찾을 수 없습니다",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    review.feedid = feed_id
    created_review = review_crud.create_review(db=db, review=review)
    return GenericResponse.success_response(created_review)

@router.get("/{feed_id}/reviews", response_model=GenericResponse[ReviewListResponse])
def get_feed_reviews(
    feed_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """피드의 리뷰 목록과 평균 평점 조회"""
    # 리뷰 목록 조회
    reviews = review_crud.get_reviews_by_feed(db, feed_id=feed_id, skip=skip, limit=limit)
    
    # 평균 평점 조회
    avg_score = review_crud.get_average_rating_by_feed(db, feed_id=feed_id)

    # 응답 데이터 구성
    response_data = ReviewListResponse(
        avgScore=avg_score,
        reviewList=reviews
    )
    
    return GenericResponse.success_response(response_data)

@router.get("/{feed_id}", response_model=GenericResponse[FeedResponse])
def get_feed(feed_id: int, db: Session = Depends(get_db)):
    """특정 피드 상세 조회"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if feed is None:
        return GenericResponse.error_response(
            error_message="피드를 찾을 수 없습니다",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return GenericResponse.success_response(feed)

@router.get("/{market_id}/{user_id}", response_model=GenericResponse[FeedListResponse])
def get_feeds_by_market(
    market_id: int,
    user_id: int,
    skip: int = 0, 
    limit: int = 50,
    promo_kind: str = Query(None, description="피드 타입: store, product, event"),
    db: Session = Depends(get_db)
):
    """특정 시장의 피드 목록 조회"""
    feeds_data = feed_crud.get_feeds_details_by_market(db, market_id=market_id, user_id=user_id, skip=skip, limit=limit)
    
    # Process feeds_data to create FeedInfo objects
    feed_info_list = []
    for feed_item in feeds_data:
        # Derive feedTitle from feedContent
        feed_content = feed_item.feedContent if feed_item.feedContent else ""
        feed_title = feed_content[:50] + "..." if len(feed_content) > 50 else feed_content

        feed_info_list.append(
            FeedInfo(
                feedId=feed_item.feedId,
                storeName=feed_item.storeName,
                storeImageUrl=feed_item.storeImageUrl,
                createdAt=feed_item.createdAt,
                feedTitle=feed_title,
                feedContent=feed_item.feedContent,
                feedImageUrl=feed_item.feedImageUrl,
                feedType=feed_item.feedType,
                feedLikeCount=feed_item.feedLikeCount,
                feedReviewCount=feed_item.feedReviewCount,
                isLiked=feed_item.isLiked
            )
        )
    
    return GenericResponse.success_response(FeedListResponse(feedList=feed_info_list))

# --- AI 이미지 생성 기능 ---

image_service = ImageGeneratorService()

@router.post("/generate", response_model=GeneratedFeedMediaResponse, tags=["ai-images"])
async def generate_feed_media(
    db: Session = Depends(get_db),
    feedType: str = Form(...),
    mediaType: str = Form(...),
    hostId: Optional[int] = Form(None),
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

@router.post("/generate-dev", response_model=GeneratedFeedMediaResponse, tags=["ai-images"])
async def generate_feed_media_dev(
    db: Session = Depends(get_db),
    feedType: str = Form(...),
    mediaType: str = Form(...),
    hostId: Optional[int] = Form(None),
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
    """피드 타입에 따라 프롬프트를 생성하고 AI 이미지를 생성합니다. (개발용)"""
    prompt = ""
    body_text = ""
    input_image: Optional[UploadFile] = None

    if mediaType == "video":
        return GenericResponse.error_response(
            error_message="비디오 생성은 현재 지원되지 않습니다.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if feedType == "store":
        if not all([hostId, storeDescription, storeImage]):
            return GenericResponse.error_response(
                error_message="'store' 타입에 필요한 필드가 누락되었습니다.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        stores = store_crud.get_stores_by_host(db, host_id=hostId)
        if not stores:
            return GenericResponse.error_response(
                error_message="상점을 찾을 수 없습니다.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        store = stores[0]
        prompt = image_service.create_store_prompt(store.storeName, storeDescription)
        body_text = storeDescription
        input_image = storeImage

    elif feedType == "product":
        if not all([hostId, productName, categoryId, productDescription, productImage]):
            return GenericResponse.error_response(
                error_message="'product' 타입에 필요한 필드가 누락되었습니다.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        stores = store_crud.get_stores_by_host(db, host_id=hostId)
        if not stores:
            return GenericResponse.error_response(
                error_message="상점을 찾을 수 없습니다.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        store = stores[0]
        prompt = image_service.create_product_prompt(productName, productDescription, store.storeName)
        body_text = f"{productName}: {productDescription}"
        input_image = productImage

    elif feedType == "event":
        if not all([eventName, eventDescription, eventStartAt, eventEndAt, eventImage]):
            return GenericResponse.error_response(
                error_message="'event' 타입에 필요한 필드가 누락되었습니다.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        prompt = image_service.create_event_prompt(eventName, eventDescription)
        body_text = f"{eventName}: {eventDescription}"
        input_image = eventImage

    else:
        return GenericResponse.error_response(
            error_message="잘못된 'feedType'입니다.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if input_image:
        await image_service.save_uploaded_file(input_image)

    generation_result = await image_service.generate_image(prompt)

    if not generation_result["success"]:
        return GenericResponse.error_response(
            error_message=generation_result.get("error", "이미지 생성에 실패했습니다."),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return GeneratedFeedMediaResponse(
        responseDto=FeedMediaResponseData(
            feedMediaUrl=generation_result["mediaUrl"],
            feedBody=body_text
        ),
        success=True
    )

@router.post("/dev", response_model=GenericResponse[FeedResponse])
def create_feed_dev(feed: FeedCreate, db: Session = Depends(get_db)):
    """새 피드 생성 (개발용)"""
    created_feed = feed_crud.create_feed(db=db, feed=feed)
    return GenericResponse.success_response(created_feed)
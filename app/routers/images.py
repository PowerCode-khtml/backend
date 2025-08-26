"""
이미지 생성 라우터 (해커톤 AI 기능)
"""
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
import os

from app.database import get_db
from app.schemas.image import ImageGenerationRequest, ImageGenerationResponse, QuickPosterRequest
from app.services.image_generator import ImageGeneratorService
from app.crud import store as store_crud, feed as feed_crud

router = APIRouter(prefix="/images", tags=["ai-images"])

# 이미지 생성 서비스 인스턴스
image_service = ImageGeneratorService()

# 상점 기반 빠른 포스터 생성
@router.post("/quick-poster", response_model=ImageGenerationResponse)
async def generate_quick_poster(
    request: QuickPosterRequest,
    db: Session = Depends(get_db)
):
    """상점 정보를 활용한 빠른 포스터 생성 (해커톤 핵심 기능)"""
    try:
        # 상점 정보 조회
        store = store_crud.get_store(db, store_id=request.storeid)
        if not store:
            raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다")
        
        # 빠른 포스터 생성
        result = await image_service.quick_store_poster(
            store_name=store.storeName,
            store_description=store.description,
            category="상점",  # 단순화
            message=request.message,
            style=request.style or "modern"
        )
        
        if result["success"]:
            # 성공시 피드로 자동 등록
            feed_data = {
                "storeid": request.storeid,
                "promoKind": "store",
                "mediaType": "image",
                "prompt": result.get("prompt_used", ""),
                "mediaUrl": result["mediaUrl"],
                "body": request.message
            }
            
            # 피드 생성을 위한 임시 객체
            from app.schemas.feed import FeedCreate
            feed_create = FeedCreate(**feed_data)
            new_feed = feed_crud.create_feed(db, feed=feed_create)
            
            result["feedid"] = new_feed.feedid
            
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"포스터 생성 실패: {str(e)}",
            "error": str(e)
        }

# AI 이미지 생성 (고급)
@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_ai_image(
    request: ImageGenerationRequest,
    db: Session = Depends(get_db)
):
    """AI 이미지 생성 (상품/이벤트 전용)"""
    try:
        # 상점 정보 조회
        store = store_crud.get_store(db, store_id=request.storeid)
        if not store:
            raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다")
        
        # 프롬프트 생성
        if request.promoKind == "product":
            prompt = image_service.create_product_prompt(
                product_name=request.productName or "상품",
                product_description=request.productDescription or "맛있는 상품",
                store_name=store.storeName
            )
        elif request.promoKind == "event":
            prompt = image_service.create_event_prompt(
                event_name=request.eventName or "이벤트",
                event_description=request.eventDescription or "특별한 이벤트",
                store_name=store.storeName
            )
        else:
            prompt = image_service.create_store_prompt(
                store_name=store.storeName,
                store_description=store.description,
                category="상점"
            )
        
        # 이미지 생성
        result = await image_service.generate_feed_image(prompt, request.promoKind)
        
        if result["success"]:
            # 피드 자동 등록
            feed_data = {
                "storeid": request.storeid,
                "promoKind": request.promoKind,
                "mediaType": "image",
                "prompt": prompt,
                "mediaUrl": result["mediaUrl"],
                "body": f"AI가 생성한 {request.promoKind} 포스터"
            }
            
            from app.schemas.feed import FeedCreate
            feed_create = FeedCreate(**feed_data)
            new_feed = feed_crud.create_feed(db, feed=feed_create)
            
            result["feedid"] = new_feed.feedid
            
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"이미지 생성 실패: {str(e)}",
            "error": str(e)
        }

# 생성된 이미지 다운로드
@router.get("/download/{filename}")
async def download_image(filename: str):
    """생성된 이미지 다운로드"""
    file_path = os.path.join("/app/generated", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="image/png"
    )

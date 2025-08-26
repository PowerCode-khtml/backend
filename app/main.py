"""
해커톤용 FastAPI 마켓플레이스 + AI 이미지 생성 애플리케이션
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import engine
from app.models import *  # 모든 모델 import
from app.routers import (
    auth_router,
    feeds_router,
    stores_router,
    images_router, 
    users_router
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="해커톤 마켓플레이스 API + AI",
    description="피드 기반 마켓플레이스 + OpenAI 이미지 생성 (해커톤 2024)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정 (해커톤용 - 모든 오리진 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 해커톤용 - 실제 배포시에는 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (생성된 이미지)
if not os.path.exists("generated"):
    os.makedirs("generated")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

# 라우터 등록
app.include_router(auth_router, prefix="/api")
app.include_router(feeds_router, prefix="/api")  # 핵심 기능
app.include_router(stores_router, prefix="/api")
app.include_router(images_router, prefix="/api")  # AI 특별 기능
app.include_router(users_router, prefix="/api")

# 홈 엔드포인트
@app.get("/")
def read_root():
    return {
        "message": "🎉 마켓플레이스 API + AI 이미지 생성",
        "version": "1.0.0",
        "docs": "/docs",
        "features": {
            "authentication": "사용자/호스트 인증",
            "feeds": "피드 시스템 (핵심)",
            "ai_images": "OpenAI 이미지 생성",
            "stores": "상점 관리",
            "reviews": "리뷰 시스템"
        },
        "endpoints": {
            "auth": "/api/auth",
            "feeds": "/api/feeds",  # 해커톤 핵심
            "stores": "/api/stores",
            "ai_images": "/api/images",  # AI 특별 기능
            "users": "/api/users"
        }
    }

# 헬스체크 엔드포인트
@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "hackathon-marketplace-api",
        "database": "connected",
        "ai_images": "available"
    }

# 해커톤 전용 엔드포인트 (데모용)
@app.get("/hackathon")
def hackathon_info():
    return {
        "event": "해커톤 2024",
        "team": "마켓플레이스 팀",
        "features": [
            "✨ AI 이미지 생성",
            "📱 피드 기반 마켓플레이스", 
            "🏪 상점 관리",
            "❤️ 좋아요 & 리뷰 시스템",
            "🔐 사용자/호스트 인증"
        ],
        "api_docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True  # 개발용 - 파일 변경시 자동 재시작
    )

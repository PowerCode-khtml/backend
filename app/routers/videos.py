"""
비디오 라우터
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.video import VideoInfo, VideoListResponse
from app.schemas.base_response import GenericResponse
from app.crud import video as video_crud

router = APIRouter(prefix="/video", tags=["videos"])

@router.get("/", response_model=GenericResponse[VideoListResponse])
def get_video_list(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    비디오 피드 목록 조회
    """
    videos_data = video_crud.get_videos(db, skip=skip, limit=limit)
    
    video_info_list = [VideoInfo.model_validate(video) for video in videos_data]
    
    return GenericResponse.success_response(VideoListResponse(videoList=video_info_list))

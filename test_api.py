#!/usr/bin/env python3
"""
해커톤용 API 테스트 스크립트
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """헬스체크 테스트"""
    print("🔍 헬스체크 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("  ✅ 서버 정상 작동")
            print(f"     {response.json()}")
        else:
            print(f"  ❌ 헬스체크 실패: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 연결 실패: {e}")

def test_auth():
    """인증 테스트"""
    print("\n👤 사용자 인증 테스트...")
    
    # 사용자 회원가입
    user_data = {
        "email": "test@hackathon.com",
        "name": "해커톤 테스터",
        "password": "hackathon2024"
    }
    
    try:
        # 회원가입
        response = requests.post(f"{BASE_URL}/api/auth/users/register", json=user_data)
        if response.status_code == 200:
            user = response.json()
            print(f"  ✅ 사용자 가입 성공: {user['name']}")
            
            # 로그인 테스트
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            
            login_response = requests.post(f"{BASE_URL}/api/auth/users/login", json=login_data)
            if login_response.status_code == 200:
                token = login_response.json()
                print(f"  ✅ 로그인 성공: {token['user_type']}")
                return token
            else:
                print("  ❌ 로그인 실패")
        else:
            print(f"  ❌ 회원가입 실패: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ 인증 테스트 실패: {e}")
    
    return None

def test_feeds():
    """피드 테스트 (해커톤 핵심)"""
    print("\n📱 피드 시스템 테스트...")
    
    try:
        # 피드 목록 조회
        response = requests.get(f"{BASE_URL}/api/feeds/")
        if response.status_code == 200:
            feeds = response.json()
            print(f"  ✅ 피드 목록 조회 성공: {len(feeds)}개 피드")
        else:
            print(f"  ❌ 피드 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ 피드 테스트 실패: {e}")

def test_ai_image():
    """AI 이미지 생성 테스트 (해커톤 특별 기능)"""
    print("\n🎨 AI 이미지 생성 테스트...")
    
    # 간단한 포스터 생성 요청
    poster_data = {
        "storeid": 1,  # 테스트용 상점 ID
        "message": "해커톤 특별 할인!",
        "style": "modern"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/images/quick-poster", json=poster_data)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"  ✅ AI 포스터 생성 성공!")
                print(f"     피드 ID: {result.get('feedid')}")
                print(f"     이미지 URL: {result.get('mediaUrl')}")
            else:
                print(f"  ⚠️ AI 기능 비활성화: {result.get('message')}")
        else:
            print(f"  ❌ AI 이미지 생성 실패: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ AI 이미지 테스트 실패: {e}")

def main():
    print("🧪 해커톤 API 테스트 시작\n")
    
    test_health()
    token = test_auth()
    test_feeds()
    test_ai_image()
    
    print("\n✅ 테스트 완료!")
    print("\n🎉 해커톤용 기능들:")
    print("  - 사용자/호스트 인증")
    print("  - 피드 시스템 (좋아요, 리뷰)")
    print("  - AI 이미지 생성")
    print("  - 상점 관리")
    print("\n📋 API 문서: http://localhost:8000/docs")
    print("🎯 해커톤 정보: http://localhost:8000/hackathon")

if __name__ == "__main__":
    main()

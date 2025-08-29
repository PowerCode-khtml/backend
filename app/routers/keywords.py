from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import json
import os

from app.schemas.keyword import KeywordResponse, KeywordListDto, KeywordItem, MarketInfoByKeyword
from app.schemas.base_response import GenericResponse

router = APIRouter(prefix="/keyword", tags=["keywords"])

# Load market data once when the application starts
# Adjust the path to market_keywords.json based on your project structure
# Assuming market_keywords.json is in the same directory as main.py or accessible from the project root
# For this example, I'll assume it's at the project root as per the user's provided path.

# Construct the absolute path to market_keywords.json
# The project root is /home/teom142/goinfre/study/market/backend/
# The file is at /home/teom142/goinfre/study/market/backend/market_keywords.json

MARKET_KEYWORDS_PATH = "./market_keywords.json"

try:
    with open(MARKET_KEYWORDS_PATH, 'r', encoding='utf-8') as f:
        market_data = json.load(f)
except FileNotFoundError:
    market_data = {}
    print(f"Error: market_keywords.json not found at {MARKET_KEYWORDS_PATH}")
except json.JSONDecodeError:
    market_data = {}
    print(f"Error: Could not decode market_keywords.json at {MARKET_KEYWORDS_PATH}")

@router.get("/", response_model=KeywordResponse)
def get_random_keywords_api():
    """랜덤 키워드 목록 조회"""
    if not market_data:
        return KeywordResponse(
            responseDto=KeywordListDto(keywordList=[]),
            success=False,
            error="Market keywords data not loaded."
        )

    selected_markets = random.sample(list(market_data.items()), min(3, len(market_data)))
    keyword_list = []

    for market, data in selected_markets:
        keywords = data.get("키워드", [])
        if keywords:
            random_keyword_entry = random.choice(keywords)
            # Assuming the keyword entry is a dictionary with a single key-value pair
            keyword_name = list(random_keyword_entry.keys())[0]
            keyword_list.append(KeywordItem(keyword=keyword_name))

    return KeywordResponse(
        responseDto=KeywordListDto(keywordList=keyword_list),
        success=True
    )

@router.get("/{keywordName}", response_model=GenericResponse[MarketInfoByKeyword])
def get_market_info_by_keyword_api(keywordName: str):
    """키워드에 해당하는 시장 정보 조회"""
    if not market_data:
        return GenericResponse.error_response("Market keywords data not loaded.")

    for market, data in market_data.items():
        for keyword_entry in data.get("키워드", []):
            # keyword_entry is a dictionary like {"keyword_name": "description"}
            for k_name, k_description in keyword_entry.items():
                if k_name == keywordName:
                    return GenericResponse.success_response(
                        MarketInfoByKeyword(marketName=market, description=k_description)
                    )
    
    return GenericResponse.error_response(f"Market information for keyword '{keywordName}' not found.")

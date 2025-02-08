import os

from fastapi import APIRouter, Depends
from pymongo import MongoClient
from ..utils.sort import sort_by_profitability

router = APIRouter()

def get_mongodb_client() -> MongoClient:
    """Dependency to get MongoDB client."""
    return MongoClient(os.getenv("MONGODB_URI"))

@router.get("/sentiment/list", response_model=list)
def get_sentiment_list(mongodb_client: MongoClient = Depends(get_mongodb_client)):
    """Get a sorted list of forex sentiment data from MongoDB."""
    mydb = mongodb_client[os.getenv("FOREX_SENTIMENT_MONGODB_DATABASE")]
    mycol = mydb[os.getenv("FOREX_SENTIMENT_MONGODB_COLLECTION")]

    sentiment_list = list(mycol.find())
    
    # Sort by profitability_percentage
    sentiment_list = sort_by_profitability(sentiment_list)

    return sentiment_list

@router.get("/sentiment/detail/{name}", response_model=dict | None)
def get_sentiment_detail(name: str, mongodb_client: MongoClient = Depends(get_mongodb_client)):
    """Get detailed sentiment data for a specific forex pair."""
    mydb = mongodb_client[os.getenv("FOREX_SENTIMENT_MONGODB_DATABASE")]
    mycol = mydb[os.getenv("FOREX_SENTIMENT_MONGODB_COLLECTION")]

    sentiment_detail = mycol.find_one({"name": name})

    return sentiment_detail
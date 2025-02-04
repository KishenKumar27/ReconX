from typing import Dict, List
from pydantic import BaseModel
from fastapi import Request, APIRouter, Query
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class NewsSource(BaseModel):
    title: str
    url: str
    image: str

class ForexAnalysisResponse(BaseModel):
    name: str
    profitability_percentage: str
    reason: str
    recommendation: str
    news_sources: List[NewsSource]

@router.get("/sentiment", response_model=ForexAnalysisResponse)
def get_forex_sentiment(
    request: Request,
    pair: str = Query(..., title="The forex pair to get sentiment for")
) -> Dict[str, str]:
    # Access forex_analyzer from the app's state
    forex_analyzer = request.app.state.forex_analyzer
    return forex_analyzer.get_sentiment(name=pair)
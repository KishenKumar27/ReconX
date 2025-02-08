from typing import Dict, List
from pydantic import BaseModel
from fastapi import Request, APIRouter, Query
from db_connection.db_utils import (
    insert_or_update_dispute,
    insert_log
)
from datetime import datetime
from src.core.dispute_analyzer import DisputeAnalyzer

router = APIRouter()

class DisputeAnalysisResponse(BaseModel):
    trade_id: int
    description: str

@router.post("/report_trade")
def report_dispute(
        input_data: DisputeAnalysisResponse
    ):
    insert_or_update_dispute(input_data.trade_id, 1, input_data.description, "pending", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # Current timestamp
    insert_log(input_data.trade_id, "Dispute reported by forex_trader", 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # Current timestamp
    dispute_analyzer = DisputeAnalyzer()
    category_name = dispute_analyzer.identify_category(input_data.description)
    print(category_name)
    
    
    return {
        "status": "success",
        "message": "Dispute reported successfully",
        "trade_id": input_data.trade_id,
        "description": input_data.description,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
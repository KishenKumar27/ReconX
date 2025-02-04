from typing import Dict, List
from pydantic import BaseModel
from fastapi import Request, APIRouter, Query

router = APIRouter()

class DisputeAnalysisResponse(BaseModel):
    trade_id: int
    description: str

@router.post("/report_trade", )
def get_dispute(
input_data: DisputeAnalysisResponse):
    return input_data
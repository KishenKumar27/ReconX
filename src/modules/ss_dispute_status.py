from pydantic import BaseModel
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from db_connection.db_utils import (
    fetch_logs
)
from datetime import datetime
import asyncio
import json

router = APIRouter()

class DisputeStatusResponse(BaseModel):
    dispute_id: int

# AI Analysis Simulation
def generate_ai_analysis():
    return {
        "type": "return",
        "Analysis": "The trade was executed at 1.2000, while the order was placed at 1.1950. This discrepancy indicates an Execution Error, likely caused by a system glitch or slippage.",
        "Dispute Category": "Execution Error",
        "Recommended Resolution": "Re-execute the trade at the correct price of 1.1950. Compensate the trader for the loss incurred due to the incorrect execution."
    }

# Function to convert datetime to string
def convert_datetime_to_str(data):
    if isinstance(data, datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")  # Adjust format as needed
    return data  # Return the value unchanged if it's not a datetime


async def event_generator(dispute_id):
    last_timestamp = "1970-01-01 00:00:00"
    while True:
        try:
            logs = fetch_logs(last_timestamp, dispute_id)
            if logs:
                for log in logs:
                    # Convert datetime values to string before using
                    log = {key: convert_datetime_to_str(value) for key, value in log.items()}
                    
                    # Update last_timestamp after processing the log
                    last_timestamp = log["timestamp"]

                    # Check that the timestamp is in string format now
                    print(f"Processed log: {log}")

                    event_data = {
                        "type": "info",
                        "dispute_id": log["dispute_id"],
                        "action": log["action"],
                        "timestamp": log["timestamp"]
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
                    await asyncio.sleep(0.5)  # Short delay to prevent excessive queries
                    
                    # Stop the loop if the action is "AI recommended re-execution"
                    if log["action"] == "AI recommended re-execution":
                        print(f"Action 'AI recommended re-execution' encountered, stopping stream for dispute_id: {dispute_id}")
                        return  # Stop the generator
            else:
                print("No logs to stream, retrying...")
                await asyncio.sleep(2)  # Wait before checking again
        except Exception as e:
            print(f"Error in event generator: {e}")
            await asyncio.sleep(2)  # Wait before retrying after an error


        
# Streaming endpoint with dispute_id as query parameter
@router.get("/stream-logs")
async def stream_logs(dispute_id: int = Query(..., description="The dispute ID to stream logs for")):
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(event_generator(dispute_id), media_type="text/event-stream", headers=headers)
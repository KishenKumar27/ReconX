import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.core.analyzer import ForexSentimentAnalyzer
from src.modules.forex_sentiment import router as forex_sentiment_router

from vers import version

TAGS_METADATA = [
    {"name": "Forex", "description": "Operations related to forex."},
]

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle startup and shutdown events."""
    app.state.forex_analyzer = ForexSentimentAnalyzer()
    logger.info("Forex Sentiment Analyzer initialized.")
    yield


app = FastAPI(
    debug=False,
    title="Forex Sentiment Analyzer API",  # Changed the title for clarity
    summary="API for analyzing forex market sentiment, trends, and news sentiment.",  # Updated the summary
    description="""
    The **Forex Sentiment Analyzer API** provides tools for analyzing forex currency pairs based on macroeconomic indicators, 
    geopolitical events, and market sentiment.
    
    ### Key Features:
    - **Sentiment Analysis**: Analyzing forex market trends and sentiment for currency pairs like USD, EUR, GBP, etc.
    - **Macroeconomic Data Integration**: Fetching data like GDP, inflation, interest rates, and unemployment rates.
    - **Geopolitical Events Analysis**: Assessing how global events impact the forex market.
    - **Forex Trend Prediction**: Using historical data and sentiment analysis to predict market trends.
    
    This API is designed to support professional forex traders, analysts, and financial institutions with data-driven insights.
    """,
    version=version,
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # If you want to allow cookies to be sent
    allow_methods=["*"],
    allow_headers=[
        "*",
    ],  # You can customize the allowed headers or use "*" to allow any header
)

app.include_router(forex_sentiment_router, prefix="/forex", tags=["Forex"])


@app.get("/health", response_class=JSONResponse)
async def healthz():
    """
    Health check endpoint to verify the application's status.
    Returns a 200 OK status with a message if the app is healthy.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

import os

from typing import List

from datetime import datetime, timedelta
from langchain.tools import tool
from eventregistry import EventRegistry, QueryArticlesIter

@tool(return_direct=False, parse_docstring=True, error_on_invalid_docstring=False)
def search_news_articles(query: str, k: int = 1, categories: List[str] = ["dmoz/Business", "dmoz/Society"], language: str = "eng") -> List[dict]:
    """
    Search for recent news articles by topic, limiting results to the last 24 hours and avoiding blogs.

    This tool searches English-language news articles from business and society categories
    within the last 24 hours, filtering out duplicate content and blog sources. Each search returns up to
    k most relevant articles.

    Args:
        query (str): The search keywords or phrase (e.g., 'Tesla earnings' or 'interest rates').
        k (int): Maximum number of articles to retrieve (default: 1).
        categories (List[str]): News categories to search (default: ['dmoz/Business', 'dmoz/Society']).
        language (str): Article language filter (default: 'eng').

    Returns:
        List[dict]: A list of articles, each containing:
            - title (str): Article headline.
            - content (str): Full article text.
            - source (str): Original article URL.
            - images (Optional[str]): URL to article image if available.

    Raises:
        ValueError: If the EventRegistry API key is not provided.
    """
    api_key = os.getenv("NEWSAPIAI_API_KEY")

    if not api_key:
        raise ValueError("EventRegistry API key is required.")

    er = EventRegistry(apiKey=api_key)
    
    # Automatically calculate date_start (1 day before) and date_end (today)
    date_end = datetime.now().strftime("%Y-%m-%d")  # Today's date
    date_start = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")  # One day before

    api_key = os.getenv("NEWSAPIAI_API_KEY")

    if not api_key:
        raise ValueError("EventRegistry API key is required.")

    er = EventRegistry(apiKey=api_key)
    
    # Define the query structure with date filtering
    query_structure = {
        "$query": {
            "$and": [
                {"keyword": query, "keywordSearchMode": "simple"},
                {"$or": [{"categoryUri": cat} for cat in categories]},
                {"lang": language},
                {"dateStart": date_start},
                {"dateEnd": date_end}
            ]
        },
        "$filter": {
            "forceMaxDataTimeWindow": "31",
            "isDuplicate": "skipDuplicates"
        }
    }

    # Execute the query
    q = QueryArticlesIter.initWithComplexQuery(query_structure)
    articles = [
        {
            "title": article["title"],
            "content": article.get("body", ""),
            "source": article.get("url", ""),
            "images": article.get("image", None),
        }
        for article in q.execQuery(er, maxItems=k)
        if "blog" not in article.get("url", "").lower()  # Filter out blog URLs
            and "tradingview.com" not in article.get("url", "").lower()  # Filter out TradingView URLs
    ]

    return articles
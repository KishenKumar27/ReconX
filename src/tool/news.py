import os

from typing import List

from langchain.tools import tool
from eventregistry import EventRegistry, QueryArticlesIter


@tool(return_direct=False, parse_docstring=True, error_on_invalid_docstring=False)
def search_news_articles(query: str, k: int = 1, categories: List[str] = ["dmoz/Business", "dmoz/Society"], language: str = "eng") -> List[dict]:
    """
    Search for recent news articles by topic.

    This tool searches English-language news articles from business and society categories
    within the last 31 days, filtering out duplicate content. Each search returns up to
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
    query_structure = {
        "$query": {
            "$and": [
                {"keyword": query, "keywordSearchMode": "simple"},
                {"$or": [{"categoryUri": cat} for cat in categories]},
                {"lang": language},
            ]
        },
        "$filter": {
            "forceMaxDataTimeWindow": "31",
            "isDuplicate": "skipDuplicates"
        }
    }

    q = QueryArticlesIter.initWithComplexQuery(query_structure)
    articles = [
        {
            "title": article["title"],
            "content": article.get("body", ""),
            "source": article.get("url", ""),
            "images": article.get("image", None),
        }
        for article in q.execQuery(er, maxItems=k)
    ]

    return articles
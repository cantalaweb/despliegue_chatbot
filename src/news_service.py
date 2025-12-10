"""
News Service module for fetching recent news using NewsAPI.
"""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class NewsService:
    """Service for fetching news from NewsAPI."""

    def __init__(self, api_key: str = None):
        """
        Initialize NewsAPI service.

        Args:
            api_key: NewsAPI key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"

    def is_available(self) -> bool:
        """Check if news service is available (API key configured)."""
        return self.api_key is not None

    def search_news(self, query: str, language: str = "es",
                   days_back: int = 7, max_results: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Search for recent news articles.

        Args:
            query: Search term (e.g., "pokemon", "futbol")
            language: Language code (es, en, etc.)
            days_back: How many days back to search
            max_results: Maximum number of results

        Returns:
            List of news articles or None if API key not configured
        """
        if not self.is_available():
            return None

        # Calculate from_date
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        try:
            response = requests.get(
                f"{self.base_url}/everything",
                params={
                    "q": query,
                    "language": language,
                    "from": from_date,
                    "sortBy": "publishedAt",
                    "pageSize": max_results,
                    "apiKey": self.api_key
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])

                # Format results
                return [
                    {
                        "title": article.get("title"),
                        "description": article.get("description"),
                        "url": article.get("url"),
                        "published_at": article.get("publishedAt"),
                        "source": article.get("source", {}).get("name")
                    }
                    for article in articles
                ]
            else:
                print(f"NewsAPI error: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return None

    def format_news_for_prompt(self, news_articles: List[Dict[str, Any]]) -> str:
        """
        Format news articles for inclusion in LLM prompt.

        Args:
            news_articles: List of news article dictionaries

        Returns:
            Formatted string with news summaries
        """
        if not news_articles:
            return "No se encontraron noticias recientes."

        formatted = []
        for i, article in enumerate(news_articles, 1):
            formatted.append(
                f"{i}. {article['title']}\n"
                f"   Fuente: {article['source']}\n"
                f"   {article['description'][:200] if article['description'] else 'Sin descripción'}..."
            )

        return "\n\n".join(formatted)

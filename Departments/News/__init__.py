"""
News Department - Sentiment Analysis & News Caching

Responsibilities:
- Fetch and cache news for stocks
- Generate sentiment scores using Perplexity AI
- Maintain 16-hour cache freshness
- Provide sentiment data to other departments
"""

from .news_department import NewsDepartment

__all__ = ['NewsDepartment']

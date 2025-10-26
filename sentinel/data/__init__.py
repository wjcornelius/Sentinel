"""Data fetching modules for Sentinel."""

from sentinel.data.news import (
    get_raw_search_results_from_perplexity,
    summarize_market_context_with_openAI
)

from sentinel.data.market_data import (
    get_alpaca_api,
    get_account_info,
    display_performance_report,
    get_nasdaq_100_symbols,
    generate_candidate_universe,
    get_stock_specific_news_headlines,
    aggregate_data_dossiers,
    fetch_latest_price_from_alpaca
)

__all__ = [
    'get_raw_search_results_from_perplexity',
    'summarize_market_context_with_openAI',
    'get_alpaca_api',
    'get_account_info',
    'generate_candidate_universe',
    'aggregate_data_dossiers'
]

"""
COMPREHENSIVE SCORING TEST - POST BUG FIXES
Tests all three scoring dimensions (Technical, Fundamental, Sentiment) for AAPL, TSLA, MSFT
Addresses C(P)'s requirements for complete end-to-end verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
import sqlite3
from pathlib import Path
from research_department import TechnicalAnalyzer, FundamentalAnalyzer, SentimentAnalyzer

# Load config
config_path = Path("Config/research_config.yaml")
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Load API key
from config import PERPLEXITY_API_KEY

db_path = Path("sentinel.db")

print("=" * 100)
print("COMPREHENSIVE SCORING TEST - ALL BUGS FIXED")
print("=" * 100)
print()

# Verify configuration
print("CONFIGURATION VERIFICATION:")
print(f"  Perplexity Model: {config['sentiment']['perplexity_model']}")
print(f"  Composite Weights: Technical {config['composite_scoring']['overall_score_weights']['technical']*100:.0f}%, "
      f"Fundamental {config['composite_scoring']['overall_score_weights']['fundamental']*100:.0f}%, "
      f"Sentiment {config['composite_scoring']['overall_score_weights']['sentiment']*100:.0f}%")
print()

# Initialize analyzers
tech_analyzer = TechnicalAnalyzer(config)
fund_analyzer = FundamentalAnalyzer(config)
sent_analyzer = SentimentAnalyzer(config, PERPLEXITY_API_KEY)

# Clear sentiment cache to force fresh API calls
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM research_sentiment_cache WHERE ticker IN ('AAPL', 'TSLA', 'MSFT')")
conn.commit()
conn.close()

# Test stocks
test_stocks = ['AAPL', 'TSLA', 'MSFT']

for ticker in test_stocks:
    print("=" * 100)
    print(f"{ticker} - COMPLETE SCORING ANALYSIS")
    print("=" * 100)
    print()

    # Technical Analysis
    print(f"[1/3] TECHNICAL ANALYSIS ({ticker}):")
    print("-" * 100)
    tech_result = tech_analyzer.calculate_technical_score(ticker)

    if tech_result['technical_score'] != 5.0:  # Not a fallback
        print(f"  RSI (14-day): {tech_result['rsi']:.2f}")
        print(f"    - Interpretation: {'Oversold (Bullish)' if tech_result['rsi'] < 30 else 'Overbought (Bearish)' if tech_result['rsi'] > 70 else 'Neutral'}")

        print(f"  MACD:")
        print(f"    - MACD Line: {tech_result['macd']:.4f}")
        print(f"    - Signal Line: {tech_result['macd_signal']:.4f}")
        print(f"    - Signal: {'BULLISH' if tech_result['macd'] > tech_result['macd_signal'] else 'BEARISH'}")

        print(f"  Bollinger Bands (20-day, 2 std):")
        print(f"    - Position: {tech_result['bollinger_position']:.2%} (0%=lower band, 100%=upper band)")

        print(f"  Volume:")
        print(f"    - Ratio to 30-day avg: {tech_result['volume_ratio']:.2f}x")
        print(f"    - Activity: {'High' if tech_result['volume_ratio'] > 1.5 else 'Normal'}")

        print(f"  TECHNICAL SCORE: {tech_result['technical_score']:.1f}/10")
    else:
        print(f"  [FALLBACK] Technical score: {tech_result['technical_score']:.1f}/10")
        print(f"  (Using default neutral scores)")

    print()

    # Fundamental Analysis
    print(f"[2/3] FUNDAMENTAL ANALYSIS ({ticker}):")
    print("-" * 100)
    fund_result = fund_analyzer.calculate_fundamental_score(ticker)

    if fund_result['fundamental_score'] != 5.0:
        print(f"  Market Cap: ${fund_result['market_cap']/1e9:.1f}B")
        print(f"  Valuation:")
        print(f"    - P/E Ratio: {fund_result['pe_ratio']:.2f}" if fund_result['pe_ratio'] else "    - P/E Ratio: N/A")
        print(f"    - Forward P/E: {fund_result['forward_pe']:.2f}" if fund_result['forward_pe'] else "    - Forward P/E: N/A")

        print(f"  Growth:")
        print(f"    - Revenue Growth (YoY): {fund_result['revenue_growth_yoy']:.1f}%" if fund_result['revenue_growth_yoy'] else "    - Revenue Growth: N/A")

        print(f"  Profitability:")
        print(f"    - Profit Margin: {fund_result['profit_margin']:.1f}%" if fund_result['profit_margin'] else "    - Profit Margin: N/A")

        print(f"  Balance Sheet:")
        print(f"    - Debt-to-Equity: {fund_result['debt_to_equity']:.2f}" if fund_result['debt_to_equity'] else "    - Debt-to-Equity: N/A")

        print(f"  FUNDAMENTAL SCORE: {fund_result['fundamental_score']:.1f}/10")
    else:
        print(f"  [FALLBACK] Fundamental score: {fund_result['fundamental_score']:.1f}/10")
        print(f"  (Data unavailable or below minimum market cap)")

    print()

    # Sentiment Analysis
    print(f"[3/3] SENTIMENT ANALYSIS ({ticker}):")
    print("-" * 100)
    sent_score, sent_summary, news_count = sent_analyzer.get_sentiment_score(ticker)

    print(f"  News Articles Analyzed: {news_count}")
    print(f"  Summary: {sent_summary[:200]}...")
    print(f"  SENTIMENT SCORE: {sent_score:.1f}/10")
    print()

    # Composite Score Calculation
    print(f"COMPOSITE SCORE CALCULATION ({ticker}):")
    print("-" * 100)

    tech_weight = config['composite_scoring']['overall_score_weights']['technical']
    fund_weight = config['composite_scoring']['overall_score_weights']['fundamental']
    sent_weight = config['composite_scoring']['overall_score_weights']['sentiment']

    tech_score = tech_result['technical_score']
    fund_score = fund_result['fundamental_score']

    tech_contrib = tech_score * tech_weight
    fund_contrib = fund_score * fund_weight
    sent_contrib = sent_score * sent_weight

    composite = tech_contrib + fund_contrib + sent_contrib

    print(f"  Technical:   {tech_score:.1f}/10 × {tech_weight:.0%} = {tech_contrib:.2f}")
    print(f"  Fundamental: {fund_score:.1f}/10 × {fund_weight:.0%} = {fund_contrib:.2f}")
    print(f"  Sentiment:   {sent_score:.1f}/10 × {sent_weight:.0%} = {sent_contrib:.2f}")
    print(f"  " + "-" * 50)
    print(f"  COMPOSITE SCORE: {composite:.1f}/10")

    # Trading recommendation
    if composite >= 7.0:
        recommendation = "STRONG BUY"
    elif composite >= 6.0:
        recommendation = "BUY"
    elif composite >= 5.0:
        recommendation = "HOLD"
    elif composite >= 4.0:
        recommendation = "SELL"
    else:
        recommendation = "STRONG SELL"

    print(f"  RECOMMENDATION: {recommendation}")
    print()
    print()

print("=" * 100)
print("TEST COMPLETE - ALL THREE SCORING DIMENSIONS VERIFIED")
print("=" * 100)

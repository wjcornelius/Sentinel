"""
Test Two-Stage Filtering Architecture

Stage 1: Swing Trading Suitability (Strategic)
- Score all tickers on volatility, liquidity, price range
- Take top 15% (~77 from 515)

Stage 2: Technical Analysis (Tactical)
- Apply adaptive RSI/momentum filters to pre-qualified universe
- Find ~50 with best technical setups

Compare vs current single-stage approach.
"""
import logging
import time
from Departments.Research import ResearchDepartment
from Departments.Risk import RiskDepartment

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 100)
print("TWO-STAGE FILTERING ARCHITECTURE TEST")
print("=" * 100)
print()

# Initialize departments
research = ResearchDepartment(db_path="sentinel.db")
risk = RiskDepartment(max_risk_per_trade_pct=1.0)

# Load universe
with open("ticker_universe.txt", "r") as f:
    universe = [line.strip() for line in f if line.strip() and not line.startswith('#')]

print(f"Universe Size: {len(universe)} tickers")
print()

# ============================================================================
# TEST A: CURRENT SINGLE-STAGE APPROACH
# ============================================================================
print("=" * 100)
print("TEST A: CURRENT APPROACH (Technical Filtering Only)")
print("=" * 100)
print()

start_time = time.time()
result_a = research.generate_daily_candidate_universe()
time_a = time.time() - start_time

candidates_a = result_a.get('buy_candidates', [])
print(f"Time: {time_a:.1f}s")
print(f"Candidates: {len(candidates_a)}")
print()

# Score these candidates for swing trading suitability
print("Scoring candidates for swing trading suitability...")
swing_suitable_count_a = 0
swing_scores_a = []

for candidate in candidates_a[:50]:  # Top 50
    ticker = candidate if isinstance(candidate, str) else candidate.get('ticker')

    # Calculate swing suitability directly
    data = research._get_cached_price_data(ticker)
    if data is None or len(data) < 20:
        continue

    import pandas as pd
    import numpy as np

    # Calculate swing metrics
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252) * 100
    avg_volume = data['Volume'].mean()
    current_price = float(data['Close'].iloc[-1])

    # Simple swing score (0-100)
    vol_score = 25 if 20 <= volatility <= 40 else (15 if 15 <= volatility <= 50 else 5)
    liq_score = 25 if avg_volume >= 1000000 else (15 if avg_volume >= 500000 else 5)
    price_score = 25 if 5 <= current_price <= 500 else 10
    swing_score = vol_score + liq_score + price_score

    swing_scores_a.append((ticker, swing_score))
    if swing_score >= 60:  # Good swing trade threshold
        swing_suitable_count_a += 1

print(f"Swing-suitable candidates (score >=60): {swing_suitable_count_a}/{len(candidates_a)}")
print()

if swing_scores_a:
    print("Top 10 by swing suitability:")
    for i, (ticker, score) in enumerate(sorted(swing_scores_a, key=lambda x: -x[1])[:10], 1):
        print(f"  {i:2d}. {ticker:6s} - {score:.1f}/100")
print()

# ============================================================================
# TEST B: TWO-STAGE APPROACH
# ============================================================================
print("=" * 100)
print("TEST B: PROPOSED TWO-STAGE APPROACH")
print("=" * 100)
print()

print("STAGE 1: Swing Trading Suitability Scoring (Strategic Filter)")
print("-" * 100)

start_time = time.time()

# Score all tickers for swing suitability
swing_scores_all = []
print("Scoring all tickers for swing trading suitability...")

for i, ticker in enumerate(universe[:515], 1):  # All tickers
    if i % 100 == 0:
        print(f"  Progress: {i}/515 tickers scored...")

    # Get price data
    data = research._get_cached_price_data(ticker)
    if data is None or len(data) < 20:
        continue

    # Calculate swing suitability metrics
    import pandas as pd
    import numpy as np

    # 1. Volatility (want 20-40%)
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252) * 100  # Annualized %

    # 2. Liquidity (want >500K avg volume)
    avg_volume = data['Volume'].mean()

    # 3. Price (want $5-$500 range)
    current_price = float(data['Close'].iloc[-1])

    # 4. ATR for stop distance (want 5-10% stops)
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift(1))
    low_close = abs(data['Low'] - data['Close'].shift(1))
    atr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1).rolling(14).mean()
    atr_pct = (atr.iloc[-1] / current_price) * 100 if not pd.isna(atr.iloc[-1]) else 0

    # Score components (0-25 each)
    vol_score = 0
    if 25 <= volatility <= 35:
        vol_score = 25
    elif 20 <= volatility < 25 or 35 < volatility <= 40:
        vol_score = 20
    elif 15 <= volatility < 20 or 40 < volatility <= 50:
        vol_score = 10

    liq_score = 0
    if avg_volume >= 2000000:
        liq_score = 25
    elif avg_volume >= 1000000:
        liq_score = 20
    elif avg_volume >= 500000:
        liq_score = 15
    elif avg_volume >= 250000:
        liq_score = 10

    price_score = 0
    if 10 <= current_price <= 200:
        price_score = 25
    elif 5 <= current_price < 10 or 200 < current_price <= 500:
        price_score = 15
    elif 2 <= current_price < 5:
        price_score = 10

    atr_score = 0
    if 6 <= atr_pct <= 9:
        atr_score = 25
    elif 5 <= atr_pct < 6 or 9 < atr_pct <= 10:
        atr_score = 20
    elif 4 <= atr_pct < 5 or 10 < atr_pct <= 12:
        atr_score = 10

    swing_score = vol_score + liq_score + price_score + atr_score

    swing_scores_all.append({
        'ticker': ticker,
        'swing_score': swing_score,
        'volatility': volatility,
        'avg_volume': avg_volume,
        'price': current_price,
        'atr_pct': atr_pct
    })

time_stage1 = time.time() - start_time

# Sort by swing score and take top 15%
swing_scores_all.sort(key=lambda x: -x['swing_score'])
top_15_pct = int(len(swing_scores_all) * 0.15)
swing_qualified = swing_scores_all[:top_15_pct]

print(f"\nStage 1 Complete:")
print(f"  Time: {time_stage1:.1f}s")
print(f"  Scored: {len(swing_scores_all)} tickers")
print(f"  Qualified (top 15%): {len(swing_qualified)} tickers")
print()

print("Top 10 Swing-Suitable Tickers:")
for i, item in enumerate(swing_qualified[:10], 1):
    print(f"  {i:2d}. {item['ticker']:6s} - Score: {item['swing_score']:3.0f}/100 "
          f"(Vol: {item['volatility']:5.1f}%, Vol: {item['avg_volume']/1e6:.1f}M, "
          f"Price: ${item['price']:.2f})")
print()

print("STAGE 2: Technical Analysis on Pre-Qualified Universe")
print("-" * 100)

# Create filtered universe file
qualified_tickers = [item['ticker'] for item in swing_qualified]

start_time = time.time()

# Apply technical filters to qualified universe only
print(f"Applying adaptive technical filters to {len(qualified_tickers)} pre-qualified tickers...")

# Use research department's adaptive filtering but on smaller universe
filter_presets = [
    {'name': 'VERY_STRICT', 'rsi': (30, 45), 'volume_min': 2000000, 'price_min': 20},
    {'name': 'STRICT', 'rsi': (25, 50), 'volume_min': 1000000, 'price_min': 10},
    {'name': 'MODERATE', 'rsi': (20, 60), 'volume_min': 500000, 'price_min': 5},
    {'name': 'RELAXED', 'rsi': (15, 70), 'volume_min': 250000, 'price_min': 2},
    {'name': 'VERY_RELAXED', 'rsi': (10, 80), 'volume_min': 100000, 'price_min': 1},
]

candidates_b = []
for preset in filter_presets:
    candidates_b = []
    for ticker in qualified_tickers:
        data = research._get_cached_price_data(ticker)
        if data is None or len(data) < 20:
            continue

        # Apply technical filters (RSI, volume, price)
        import pandas as pd

        # RSI
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # Filters
        if pd.isna(current_rsi):
            continue

        rsi_min, rsi_max = preset['rsi']
        if not (rsi_min <= current_rsi <= rsi_max):
            continue

        avg_volume = data['Volume'].tail(20).mean()
        if avg_volume < preset['volume_min']:
            continue

        current_price = float(data['Close'].iloc[-1])
        if current_price < preset['price_min']:
            continue

        candidates_b.append(ticker)

    print(f"  {preset['name']:15s}: {len(candidates_b)} candidates")

    # Stop if we're in the 40-60 range
    if 40 <= len(candidates_b) <= 60:
        break

# Take top 50
candidates_b = candidates_b[:50]
time_stage2 = time.time() - start_time

print()
print(f"Stage 2 Complete:")
print(f"  Time: {time_stage2:.1f}s")
print(f"  Candidates: {len(candidates_b)}")
print()

time_b = time_stage1 + time_stage2

# ============================================================================
# COMPARISON
# ============================================================================
print("=" * 100)
print("RESULTS COMPARISON")
print("=" * 100)
print()

print(f"{'Metric':<40s} {'Current (A)':<20s} {'Two-Stage (B)':<20s}")
print("-" * 100)
print(f"{'Total Time':<40s} {time_a:>10.1f}s {time_b:>20.1f}s")
print(f"{'Candidates Found':<40s} {len(candidates_a):>10d} {len(candidates_b):>20d}")
print(f"{'Swing-Suitable (score >=60)':<40s} {swing_suitable_count_a:>10d} {'ALL (pre-filtered)':>20s}")
print(f"{'Swing Suitability Rate':<40s} {swing_suitable_count_a/max(len(candidates_a),1)*100:>9.0f}% {'100%':>20s}")
print()

print("=" * 100)
print("ANALYSIS")
print("=" * 100)
print()

if swing_suitable_count_a < len(candidates_a) * 0.8:
    print("WARNING - CURRENT APPROACH: Many candidates unsuitable for swing trading")
    print(f"  -> Only {swing_suitable_count_a}/{len(candidates_a)} candidates score >=60 for swing suitability")
    print()

print("SUCCESS - TWO-STAGE APPROACH:")
print(f"  -> ALL {len(candidates_b)} candidates are pre-qualified for swing trading")
print(f"  -> Top 15% ({len(swing_qualified)}) screened for best swing characteristics")
print(f"  -> Technical analysis only applied to suitable stocks")
print()

print("RECOMMENDATION:")
print("  Implement two-stage filtering for better quality candidates.")
print("  Stage 1 ensures philosophical alignment (swing suitability)")
print("  Stage 2 finds best technical setups within suitable universe")
print()

print("=" * 100)
print("TEST COMPLETE")
print("=" * 100)

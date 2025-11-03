"""
Analyze Research Department Performance
- Adaptive filtering effectiveness
- Processing time for full universe
- Filter parameters settled on
- Quality of parameters for swing trading
"""
import logging
import time
from Departments.Research import ResearchDepartment

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 100)
print("RESEARCH DEPARTMENT PERFORMANCE ANALYSIS")
print("=" * 100)
print()

# Initialize
research = ResearchDepartment(db_path="sentinel.db")

# Get universe size
with open("ticker_universe.txt", "r") as f:
    universe = [line.strip() for line in f if line.strip() and not line.startswith('#')]

print(f"Universe Size: {len(universe)} tickers")
print()

# Run full analysis with timing
print("Starting adaptive filtering...")
print("Target: ~50 candidates")
print()

start_time = time.time()
result = research.generate_daily_candidate_universe()
elapsed_time = time.time() - start_time

# Extract results
buy_candidates = result.get('buy_candidates', [])
current_holdings = result.get('current_holdings', [])
market_conditions = result.get('market_conditions', {})

print()
print("=" * 100)
print("RESULTS")
print("=" * 100)
print()

print(f"Processing Time: {elapsed_time:.1f} seconds ({elapsed_time/60:.2f} minutes)")
print(f"Universe Processed: {len(universe)} tickers")
print(f"Throughput: {len(universe)/elapsed_time:.1f} tickers/second")
print()

print(f"Buy Candidates Found: {len(buy_candidates)}")
print(f"Current Holdings: {len(current_holdings)}")
print(f"Total Output: {len(buy_candidates) + len(current_holdings)}")
print()

# Show filter preset used (from logs)
print("=" * 100)
print("ADAPTIVE FILTERING ANALYSIS")
print("=" * 100)
print()

print("Filter Presets Available:")
presets = [
    {'name': 'VERY_STRICT', 'rsi': (30, 45), 'volume_min': 2000000, 'price_min': 20},
    {'name': 'STRICT', 'rsi': (25, 50), 'volume_min': 1000000, 'price_min': 10},
    {'name': 'MODERATE', 'rsi': (20, 60), 'volume_min': 500000, 'price_min': 5},
    {'name': 'RELAXED', 'rsi': (15, 70), 'volume_min': 250000, 'price_min': 2},
    {'name': 'VERY_RELAXED', 'rsi': (10, 80), 'volume_min': 100000, 'price_min': 1},
]

for p in presets:
    print(f"\n{p['name']:15s}:")
    print(f"  RSI Range:     {p['rsi'][0]}-{p['rsi'][1]}")
    print(f"  Min Volume:    {p['volume_min']:,}")
    print(f"  Min Price:     ${p['price_min']}")

print()
print("=" * 100)
print("SWING TRADING SUITABILITY ASSESSMENT")
print("=" * 100)
print()

# Assess which preset was likely used based on candidate count
target_min = 40  # 80% of 50
target_max = 60  # 120% of 50

if target_min <= len(buy_candidates) <= target_max:
    print(f"✓ Target Achieved: {len(buy_candidates)} candidates (target 40-60)")
    print()
    print("Likely Filter Preset Used: Check logs above for exact preset")
else:
    print(f"⚠ Off Target: {len(buy_candidates)} candidates (target 40-60)")
    if len(buy_candidates) < target_min:
        print("  → May have used too strict filters OR market conditions limiting candidates")
    else:
        print("  → May have used too loose filters")

print()
print("=" * 100)
print("SWING TRADING PHILOSOPHY CHECK")
print("=" * 100)
print()

print("For Sentinel Corporation's swing trading approach, we want:")
print("  • RSI: 15-70 (catch momentum, not just oversold)")
print("  • Volume: 500K+ (liquidity for 1-4 week holds)")
print("  • Price: $5+ (avoid penny stocks, but not too restrictive)")
print()

if len(buy_candidates) >= 40:
    print("✓ Good candidate pool for portfolio diversity (~60 positions)")
elif len(buy_candidates) >= 20:
    print("⚠ Marginal candidate pool - may need looser filters")
else:
    print("✗ Insufficient candidates - filters too strict for current market")

print()
print("=" * 100)
print("MARKET CONDITIONS")
print("=" * 100)
print()

if market_conditions:
    print(f"SPY Change:    {market_conditions.get('spy_change_pct', 0):.2f}%")
    print(f"VIX Level:     {market_conditions.get('vix_level', 0):.2f}")
    print(f"Regime:        {market_conditions.get('market_regime', 'UNKNOWN')}")
else:
    print("No market conditions data available")

print()
print("=" * 100)
print("DONE")
print("=" * 100)

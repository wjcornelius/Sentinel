# AI Model Costs - Sentinel Corporation

## OpenAI Models for Portfolio Optimization

### GPT-4o (DEFAULT - RECOMMENDED)
**Cost**: $2-3 per trading plan generation
- **Input**: $2.50 per 1M tokens
- **Output**: $10.00 per 1M tokens
- **Typical run**: ~30K input + ~2K output = **$2.10 total**
- **Speed**: 2-3 minutes
- **Quality**: Excellent for portfolio decisions
- **Monthly cost (20 trading days)**: ~$42-60

### GPT-4o-mini (BUDGET OPTION)
**Cost**: $0.50-1.00 per trading plan generation
- **Input**: $0.15 per 1M tokens
- **Output**: $0.60 per 1M tokens
- **Typical run**: ~30K input + ~2K output = **$0.46 total**
- **Speed**: 1-2 minutes
- **Quality**: Good for most decisions, may be less nuanced
- **Monthly cost (20 trading days)**: ~$10-20

### GPT-5 (PREMIUM - USE SPARINGLY)
**Cost**: $10-20 per trading plan generation
- **Input**: $10.00 per 1M tokens (+ reasoning tokens)
- **Output**: $40.00 per 1M tokens
- **Typical run**: ~30K input + ~2K output + **10K reasoning** = **$10-20 total**
- **Speed**: 10-15 minutes (extended reasoning)
- **Quality**: Best possible, but 5-10x more expensive
- **Monthly cost (20 trading days)**: ~$200-400

## Other AI Services

### Perplexity API (News Sentiment)
**Cost**: Included in $20/month subscription
- Already being used
- No additional cost per run
- Cached for 16 hours

## Recommendations by Budget

### Tight Budget (<$20/month AI costs) ✅ **CURRENT DEFAULT**
- **Portfolio Optimizer**: GPT-4o-mini ($0.50/run)
- **Monthly**: ~$10-20 for 20 trading days
- **Quality**: Good enough for most decisions
- **Best for**: SSI/fixed income, testing, daily trading

### Moderate Budget ($50-100/month AI costs)
- **Portfolio Optimizer**: GPT-4o ($2-3/run)
- **Monthly**: ~$40-60 for 20 trading days
- **Quality**: Excellent balance of cost and performance
- **Best for**: When you need more sophisticated reasoning

### Premium (>$100/month AI costs)
- **Portfolio Optimizer**: GPT-5 ($10-20/run)
- **Monthly**: ~$200-400 for 20 trading days
- **Quality**: Best possible, but only if budget allows
- **Best for**: Large portfolios, critical rebalancing decisions

## How to Change Models

### Temporary (One-Time Change)
Currently requires code edit - coming soon: control panel option

### Permanent (Change Default)
Edit `operations_manager.py` line 631:
```python
self._gpt5_optimizer = GPT5PortfolioOptimizer(
    api_key=app_config.OPENAI_API_KEY,
    model="gpt-4o-mini"  # Change to "gpt-4o" or "gpt-5" if budget allows
)
```

## Cost Tracking

### Today's Costs (November 4, 2025)
- Multiple test runs with GPT-5: **~$30-50 estimated**
- This is NOT sustainable on SSI budget

### Going Forward (with GPT-4o-mini default)
- Daily cost: $0.50 per trading day
- Monthly cost: $10-20 per month (20 trading days)
- **Sustainable on SSI budget**

## Alternative APIs Considered

### Poe API
- ❌ **No public API exists** - only chat interface for consumers
- Your $19.99/month subscription cannot be used for programmatic access
- Reverse engineering violates TOS

### OpenRouter
- ✅ Real API with multi-model access
- ✅ Transparent per-token pricing
- ❌ **No auto-recharge** - dealbreaker for managing on SSI
- Would require manual balance top-ups

### Decision
Staying with **OpenAI direct API** because:
1. Auto-charges credit card (no manual recharges)
2. Reliable, official, well-documented
3. GPT-4o-mini is affordable enough ($10-20/month)

---

*Last Updated: November 4, 2025*
*Default Model: GPT-4o-mini*
*Monthly Budget: $10-20 (SSI-friendly)*

"""Check actual Alpaca paper trading account status"""
import sys
sys.path.insert(0, '.')
import config
import alpaca_trade_api as tradeapi

# Initialize Alpaca (old API)
api = tradeapi.REST(
    config.ALPACA_API_KEY,
    config.ALPACA_SECRET_KEY,
    config.ALPACA_BASE_URI,
    api_version='v2'
)

# Get account info
account = api.get_account()
print('=' * 70)
print('ALPACA PAPER TRADING ACCOUNT (ACTUAL):')
print('=' * 70)
print(f'Portfolio Value: ${float(account.portfolio_value):,.2f}')
print(f'Cash: ${float(account.cash):,.2f}')
print(f'Equity: ${float(account.equity):,.2f}')
print(f'Buying Power: ${float(account.buying_power):,.2f}')
print()

# Get positions
positions = api.list_positions()
print(f'OPEN POSITIONS ({len(positions)}):')
print('=' * 70)
if positions:
    total_value = 0
    total_unrealized = 0
    for pos in positions:
        market_value = float(pos.market_value)
        unrealized_pl = float(pos.unrealized_pl)
        pct = float(pos.unrealized_plpc) * 100
        total_value += market_value
        total_unrealized += unrealized_pl
        print(f'{pos.symbol:6} | {pos.qty:>4} shares @ ${float(pos.avg_entry_price):>7.2f} | Value: ${market_value:>10,.2f} | P&L: ${unrealized_pl:>9,.2f} ({pct:+6.2f}%)')
    print('=' * 70)
    print(f'TOTAL  | {len(positions)} positions | Value: ${total_value:>10,.2f} | P&L: ${total_unrealized:>9,.2f}')
else:
    print('No open positions')
print('=' * 70)

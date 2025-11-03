"""
Test Bracket Order Implementation
==================================
Quick test to verify bracket order calculation logic

This tests the bracket order parameters without actually submitting to Alpaca.
"""

def calculate_bracket_prices(entry_price: float, stop_loss_pct: float = 0.08, take_profit_pct: float = 0.16):
    """
    Calculate bracket order prices

    Args:
        entry_price: Expected entry price
        stop_loss_pct: Stop loss percentage below entry (default 8%)
        take_profit_pct: Take profit percentage above entry (default 16%)

    Returns:
        (stop_loss_price, take_profit_price)
    """
    stop_loss_price = round(entry_price * (1 - stop_loss_pct), 2)
    take_profit_price = round(entry_price * (1 + take_profit_pct), 2)
    return stop_loss_price, take_profit_price


def test_bracket_orders():
    """Test bracket order calculations with sample stock prices"""

    test_cases = [
        ("CARR", 59.49),
        ("CCL", 28.83),
        ("COP", 88.86),
        ("EIX", 55.38),
        ("FITB", 41.62),
        ("GLW", 89.08),
        ("HPQ", 27.67),
        ("IBKR", 70.36),
        ("ODFL", 140.42),
    ]

    print("=" * 80)
    print("BRACKET ORDER TEST - WIDE BRACKETS for 'Room to Run'")
    print("=" * 80)
    print("\nStop-Loss: 8% below entry | Take-Profit: 16% above entry")
    print("Philosophy: Volatile swing stocks need breathing room\n")

    for ticker, entry_price in test_cases:
        stop_loss, take_profit = calculate_bracket_prices(entry_price)

        # Calculate actual percentages for verification
        actual_stop_pct = ((entry_price - stop_loss) / entry_price) * 100
        actual_tp_pct = ((take_profit - entry_price) / entry_price) * 100
        risk_reward_ratio = actual_tp_pct / actual_stop_pct if actual_stop_pct > 0 else 0

        print(f"{ticker:6} | Entry: ${entry_price:7.2f}")
        print(f"       | Stop:  ${stop_loss:7.2f} ({actual_stop_pct:5.2f}% below)")
        print(f"       | Target: ${take_profit:7.2f} ({actual_tp_pct:5.2f}% above)")
        print(f"       | R/R Ratio: {risk_reward_ratio:.2f}:1")
        print("-" * 80)


if __name__ == "__main__":
    test_bracket_orders()

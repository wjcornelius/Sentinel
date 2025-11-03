"""
Test Research Department v3.0 - DailyBriefing Message Generation
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 80)
print("TESTING RESEARCH v3.0 - DAILY BRIEFING MESSAGE GENERATION")
print("=" * 80)
print()

# Import Alpaca client for holdings
try:
    from Utils.alpaca_client import AlpacaClient
    alpaca_client = AlpacaClient()
    print("[OK] Alpaca client initialized")
except Exception as e:
    print(f"[WARN] Alpaca client failed: {e}")
    print(f"  Continuing without live holdings...")
    alpaca_client = None

# Initialize Research Department
from Departments.Research.research_department import ResearchDepartment

research = ResearchDepartment(
    db_path="sentinel.db",
    alpaca_client=alpaca_client
)
print("[OK] Research Department v3.0 initialized")
print()

# Generate daily briefing
print("Generating DailyBriefing message...")
print("-" * 80)

try:
    message_id = research.generate_daily_briefing()
    print("-" * 80)
    print()
    print("[SUCCESS]")
    print(f"  Message ID: {message_id}")
    print(f"  Location: Messages_Between_Departments/Outbox/RESEARCH/{message_id}.md")
    print()

    # Read and display the message
    message_file = Path(f"Messages_Between_Departments/Outbox/RESEARCH/{message_id}.md")
    if message_file.exists():
        print("=" * 80)
        print("MESSAGE CONTENT (First 1500 chars):")
        print("=" * 80)
        with open(message_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:1500])
            if len(content) > 1500:
                print(f"\n... ({len(content) - 1500} more characters)")
        print()
        print("=" * 80)
        print("[OK] Message file verified and readable")
        print("=" * 80)

except Exception as e:
    print("-" * 80)
    print()
    print(f"[FAILED]: {e}")
    import traceback
    traceback.print_exc()

"""
Fix ALL Missing Research Department Tables
===========================================
Emergency fix for missing Research Department database tables.

Creates all tables needed by Research Department to function properly.

Author: Claude Code (CC)
Date: November 1, 2025
"""

import sqlite3
from pathlib import Path

def fix_all_research_tables():
    """Create all missing Research Department tables"""

    # Database path
    db_path = Path(__file__).parent / "sentinel.db"

    print(f"\nConnecting to database: {db_path}")

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        tables_created = []

        # 1. research_sentiment_cache
        print("\n[1/2] Creating research_sentiment_cache table...")
        cursor.execute("DROP TABLE IF EXISTS research_sentiment_cache")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_sentiment_cache (
                ticker TEXT PRIMARY KEY,
                query_date DATE NOT NULL,
                sentiment_score REAL NOT NULL,
                sentiment_summary TEXT,
                news_articles_count INTEGER DEFAULT 0,
                expires_at TIMESTAMP NOT NULL
            )
        """)
        tables_created.append("research_sentiment_cache")

        # 2. research_api_calls
        print("[2/2] Creating research_api_calls table...")
        cursor.execute("DROP TABLE IF EXISTS research_api_calls")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_api_calls (
                call_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_name TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                response_status TEXT NOT NULL,
                response_time_ms REAL NOT NULL,
                error_message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        tables_created.append("research_api_calls")

        conn.commit()

        # Verify all tables were created
        print("\n" + "=" * 60)
        print("VERIFICATION")
        print("=" * 60)

        all_success = True
        for table_name in tables_created:
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name=?
            """, (table_name,))

            result = cursor.fetchone()
            if result:
                print(f"[OK] {table_name}")
            else:
                print(f"[FAIL] {table_name}")
                all_success = False

        if all_success:
            print("\n" + "=" * 60)
            print("ALL TABLES CREATED SUCCESSFULLY")
            print("=" * 60)
            print(f"\nCreated {len(tables_created)} tables:")
            for table in tables_created:
                print(f"  - {table}")
            print("\nYou can now retry generating a trading plan.")
            conn.close()
            return True
        else:
            print("\n[ERROR] Some tables failed to create!")
            conn.close()
            return False

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print(" " * 10 + "RESEARCH TABLES FIX UTILITY")
    print("=" * 60)
    print("\nFixing all missing Research Department tables...")

    success = fix_all_research_tables()

    if success:
        print("\n" + "=" * 60)
        print(" " * 20 + "FIX COMPLETE")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(" " * 20 + "FIX FAILED")
        print("=" * 60)
        print("\nPlease check the error messages above.")

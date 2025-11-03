"""
Fix Missing research_sentiment_cache Table
==========================================
Emergency fix for database schema issue discovered during live testing.

This script creates the missing research_sentiment_cache table that
Research Department's SentimentAnalyzer requires.

Author: Claude Code (CC)
Date: November 1, 2025
Issue: sqlite3.OperationalError: no such table: research_sentiment_cache
"""

import sqlite3
from pathlib import Path

def fix_sentiment_cache_table():
    """Create missing research_sentiment_cache table"""

    # Database path
    db_path = Path(__file__).parent / "sentinel.db"

    print(f"\nConnecting to database: {db_path}")

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        print("\nCreating research_sentiment_cache table...")

        # Drop existing table if it has wrong schema
        cursor.execute("DROP TABLE IF EXISTS research_sentiment_cache")

        # Create the table with correct schema (query_date not analysis_date!)
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

        conn.commit()

        # Verify table was created
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='research_sentiment_cache'
        """)

        result = cursor.fetchone()

        if result:
            print("[OK] Table 'research_sentiment_cache' created successfully!")

            # Show table schema
            cursor.execute("PRAGMA table_info(research_sentiment_cache)")
            columns = cursor.fetchall()

            print("\nTable Schema:")
            print("-" * 60)
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                print(f"  {col_name:25} {col_type:15} {'PRIMARY KEY' if pk else ''}")

            print("\n[OK] Database fix completed successfully!")
            print("\nYou can now retry generating a trading plan.")

            conn.close()
            return True
        else:
            print("ERROR: Table creation failed!")
            conn.close()
            return False

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print(" " * 15 + "DATABASE FIX UTILITY")
    print("=" * 60)
    print("\nFixing missing research_sentiment_cache table...")

    success = fix_sentiment_cache_table()

    if success:
        print("\n" + "=" * 60)
        print(" " * 20 + "FIX COMPLETE")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(" " * 20 + "FIX FAILED")
        print("=" * 60)
        print("\nPlease check the error messages above.")

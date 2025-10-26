#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Clear Today's Plan - Utility Script

Clears any incomplete or stuck plans from today's date.
Run this if Sentinel gets stuck or you want to force a fresh plan generation.
"""

import sqlite3
from datetime import datetime

DB_FILE = "sentinel.db"

def main():
    print("=" * 60)
    print("CLEAR TODAY'S PLAN UTILITY")
    print("=" * 60)
    print()

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check what exists for today
        cursor.execute("""
            SELECT COUNT(*) FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        decision_count = cursor.fetchone()[0]

        print(f"Found {decision_count} decisions for today.")

        if decision_count == 0:
            print("No decisions to clear. Database is already clean for today.")
            conn.close()
            return

        # Ask for confirmation
        print()
        print("This will DELETE:")
        print(f"  - {decision_count} decision(s) from the 'decisions' table")
        print()
        confirm = input("Type 'YES' to confirm deletion: ").strip()

        if confirm != "YES":
            print("Cancelled. No changes made.")
            conn.close()
            return

        # Delete today's decisions
        cursor.execute("""
            DELETE FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        print()
        print(f"[OK] Successfully deleted {deleted} decision(s).")
        print("You can now run Sentinel to generate a fresh plan.")
        print()

    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

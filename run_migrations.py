#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Migration Runner for Sentinel

Applies SQL migrations to sentinel.db in order.
Tracks which migrations have been applied to avoid duplicates.
"""

import sqlite3
import os
import glob
from datetime import datetime

DB_FILE = "sentinel.db"
MIGRATIONS_DIR = "database_migrations"


def create_migrations_table(conn):
    """Create table to track applied migrations."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            migration_file TEXT NOT NULL UNIQUE,
            applied_at DATETIME NOT NULL
        )
    """)
    conn.commit()


def get_applied_migrations(conn):
    """Get list of already applied migrations."""
    cursor = conn.execute("SELECT migration_file FROM schema_migrations ORDER BY migration_file")
    return {row[0] for row in cursor.fetchall()}


def apply_migration(conn, migration_file):
    """Apply a single migration file."""
    print(f"Applying migration: {migration_file}")

    with open(os.path.join(MIGRATIONS_DIR, migration_file), 'r') as f:
        sql = f.read()

    # Split by semicolon and execute each statement
    statements = [s.strip() for s in sql.split(';') if s.strip()]

    for statement in statements:
        try:
            conn.execute(statement)
        except sqlite3.Error as e:
            # If column already exists, that's OK (idempotent)
            if "duplicate column name" in str(e).lower():
                print(f"  - Column already exists, skipping")
            else:
                raise

    # Record migration as applied
    conn.execute(
        "INSERT INTO schema_migrations (migration_file, applied_at) VALUES (?, ?)",
        (migration_file, datetime.now())
    )
    conn.commit()
    print(f"  [OK] Applied successfully")


def run_migrations():
    """Run all pending migrations."""
    if not os.path.exists(DB_FILE):
        print(f"ERROR: Database file '{DB_FILE}' not found!")
        print("Run database_setup.py first to create the database.")
        return False

    print("=" * 60)
    print("Sentinel Database Migration Runner")
    print("=" * 60)

    conn = sqlite3.connect(DB_FILE)

    try:
        # Create migrations tracking table
        create_migrations_table(conn)

        # Get already applied migrations
        applied = get_applied_migrations(conn)
        print(f"\nAlready applied: {len(applied)} migration(s)")

        # Get all migration files
        migration_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))

        if not migration_files:
            print("\nNo migration files found in", MIGRATIONS_DIR)
            return True

        # Apply pending migrations
        pending = [os.path.basename(f) for f in migration_files if os.path.basename(f) not in applied]

        if not pending:
            print("\n[OK] Database is up to date. No pending migrations.")
            return True

        print(f"\nPending migrations: {len(pending)}")
        for migration_file in pending:
            apply_migration(conn, migration_file)

        print("\n" + "=" * 60)
        print(f"[SUCCESS] Applied {len(pending)} migration(s)")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    success = run_migrations()
    exit(0 if success else 1)

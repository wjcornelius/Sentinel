#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Backup Utility for Sentinel

This script creates timestamped backups of sentinel.db and maintains
a rolling window of the last 30 days of backups.

Can be run standalone or imported by main_script.py for automatic backups.
"""

import shutil
import os
from datetime import datetime, timedelta
from pathlib import Path
import logging

DB_FILE = "sentinel.db"
BACKUP_DIR = "backups"
BACKUP_RETENTION_DAYS = 30


def create_backup():
    """
    Create a timestamped backup of the database.

    Returns:
        str: Path to the backup file, or None if backup failed
    """
    if not os.path.exists(DB_FILE):
        logging.warning(f"Database file '{DB_FILE}' not found - no backup created")
        print(f"WARNING: Database file '{DB_FILE}' not found. No backup created.")
        return None

    # Create backup directory if it doesn't exist
    Path(BACKUP_DIR).mkdir(exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"sentinel_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        # Copy database file
        shutil.copy2(DB_FILE, backup_path)
        file_size = os.path.getsize(backup_path)
        logging.info(f"Database backup created: {backup_path} ({file_size:,} bytes)")
        print(f"[OK] Database backup created: {backup_path} ({file_size:,} bytes)")
        return backup_path
    except Exception as e:
        logging.error(f"Failed to create database backup: {e}", exc_info=True)
        print(f"[ERROR] Failed to create database backup: {e}")
        return None


def cleanup_old_backups():
    """
    Remove backup files older than BACKUP_RETENTION_DAYS.

    Returns:
        int: Number of old backups deleted
    """
    if not os.path.exists(BACKUP_DIR):
        return 0

    cutoff_date = datetime.now() - timedelta(days=BACKUP_RETENTION_DAYS)
    deleted_count = 0

    try:
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("sentinel_backup_") and filename.endswith(".db"):
                filepath = os.path.join(BACKUP_DIR, filename)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))

                if file_mtime < cutoff_date:
                    os.remove(filepath)
                    deleted_count += 1
                    logging.debug(f"Deleted old backup: {filename} (age: {(datetime.now() - file_mtime).days} days)")

        if deleted_count > 0:
            logging.info(f"Cleaned up {deleted_count} old backup(s) older than {BACKUP_RETENTION_DAYS} days")
            print(f"[OK] Cleaned up {deleted_count} old backup(s)")

        return deleted_count
    except Exception as e:
        logging.error(f"Error during backup cleanup: {e}", exc_info=True)
        print(f"WARNING: Error during backup cleanup: {e}")
        return deleted_count


def list_backups():
    """
    List all available database backups.

    Returns:
        list: List of tuples (filename, size_bytes, modified_time)
    """
    if not os.path.exists(BACKUP_DIR):
        return []

    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("sentinel_backup_") and filename.endswith(".db"):
            filepath = os.path.join(BACKUP_DIR, filename)
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append((filename, size, mtime))

    # Sort by modification time, newest first
    backups.sort(key=lambda x: x[2], reverse=True)
    return backups


def run_backup_maintenance():
    """
    Perform a complete backup maintenance cycle: create backup and cleanup old ones.

    This is the main function to be called from main_script.py.

    Returns:
        bool: True if backup was successful, False otherwise
    """
    logging.info("Starting database backup maintenance")

    # Create new backup
    backup_path = create_backup()
    if backup_path is None:
        return False

    # Clean up old backups
    cleanup_old_backups()

    # Show current backup count
    backups = list_backups()
    logging.info(f"Total backups retained: {len(backups)}")

    return True


if __name__ == "__main__":
    # Setup basic logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("=" * 60)
    print("Sentinel Database Backup Utility")
    print("=" * 60)

    # Run backup maintenance
    success = run_backup_maintenance()

    # List all backups
    print("\nCurrent backups:")
    backups = list_backups()
    if backups:
        for filename, size, mtime in backups:
            age_days = (datetime.now() - mtime).days
            print(f"  - {filename}: {size:,} bytes (age: {age_days} days)")
    else:
        print("  (no backups found)")

    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] Backup completed successfully")
    else:
        print("[FAILED] Backup failed")
    print("=" * 60)

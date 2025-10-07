# database_setup.py
# A one-time script to create and initialize the sentinel.db SQLite database.
# This script is NOT part of the main application workflow.

import sqlite3
import os

DB_FILE = "sentinel.db"

def create_database():
    """Creates the database file and the necessary tables if they don't exist."""
    
    # Check if the database file already exists. If so, do nothing.
    if os.path.exists(DB_FILE):
        print(f"Database file '{DB_FILE}' already exists. Setup not required.")
        return

    print(f"Creating new database file: '{DB_FILE}'...")
    
    try:
        # Connect to the database. This will create the file if it doesn't exist.
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # --- Create the 'decisions' table ---
        # This table logs every single recommendation the AI makes.
        print("Creating table: 'decisions'")
        cursor.execute("""
            CREATE TABLE decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                symbol TEXT NOT NULL,
                decision TEXT NOT NULL,
                conviction_score INTEGER,
                rationale TEXT,
                latest_price REAL,
                market_context_summary TEXT
            )
        """)

        # --- Create the 'trades' table ---
        # This table logs only the trades that are approved and executed.
        print("Creating table: 'trades'")
        cursor.execute("""
            CREATE TABLE trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decision_id INTEGER,
                timestamp DATETIME NOT NULL,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                quantity REAL NOT NULL,
                status TEXT NOT NULL,
                avg_fill_price REAL,
                alpaca_order_id TEXT,
                FOREIGN KEY (decision_id) REFERENCES decisions (id)
            )
        """)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
        print("\nDatabase and tables created successfully.")
        print(f"You can now open '{DB_FILE}' with a tool like DB Browser for SQLite.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        # If an error occurred, delete the partially created file to allow a clean retry.
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            print(f"Removed partially created file '{DB_FILE}'. Please try again.")

if __name__ == "__main__":
    create_database()
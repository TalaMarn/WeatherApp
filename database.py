import sqlite3
from pathlib import Path

# Database Loacation
BASE_DIR = Path(__file__).resolve().parent
DB_FOLDER = BASE_DIR / "database"
DB_PATH = DB_FOLDER / "weather.db"

def connect_db():
    """Connect to the SQLite database"""
    DB_FOLDER.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

def create_table():
    """Create Table"""
    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        temperature REAL,
        description TEXT,
        searched_at TEXT DEFAULT (
        datetime('now', 'localtime')
        )
    )
""")

    conn.commit()
    conn.close()

    print("Database and table create successfully!")

def save_search(city, temperature, description):
    """Save a weather search."""
    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO search_history
        (city, temperature, description)
        VALUES (?, ?, ?)
""", (city, temperature, description))

    conn.comit()
    conn.close()

    print(f"Saved weather search for {city}")

def get_history():
    """Retriveve all search history"""

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM search_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records

def delete_search(search_id):
    """Delete one search record."""
    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM search_history
        WHERE id = ?
    """, (search_id,))

    conn.commit()
    conn.close()

def clear_history():
    """Delete all search history"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM search_history")

    conn.comit()
    conn.close()

if __name__ == "__main__":
    create_table()
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "job_tracker.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# Create and returns a connection to the SQLite database
# Returns sqlite3.Connection: Active database connection object
def get_connection():
    return sqlite3.connect(DB_PATH)

# Initializes the database by executing the SQL schema file
def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # Open and rad the schema file that contains SQL table
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Saves and closes
    conn.commit()
    conn.close()

# Ensures that it is initialized when this file is run
if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database created successfully!")
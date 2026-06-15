import sqlite3

# Path to the SQLite database file
# If it doesn't exist, it will be created
DB_PATH = "data/job_tracker.db"

# Create and returns a connection to the SQLite database
# Returns sqlite3.Connection: Active database connection object
def get_connection():
    return sqlite3.connect(DB_PATH)

# Initializes the database by executing the SQL schema file
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Open and rad the schema file that contains SQL table
    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())

    # Saves and closes
    conn.commit()
    conn.close()

# Ensures that it is initialized when this file is run
if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database created successfully!")
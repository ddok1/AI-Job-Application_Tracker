from database.db import get_connection


# CREATE
def add_application(company, position, status, date_applied, notes):
    """
    Adds a new job application to the database
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (company, position, status, date_applied, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (company, position, status, date_applied, notes))

    conn.commit()
    conn.close()


# READ (ALL)
def get_all_applications():
    """
    Returns all job applications from the database
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()

    conn.close()
    return rows
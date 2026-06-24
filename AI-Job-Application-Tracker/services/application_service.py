from database.db import get_connection


# CREATE
def add_application(company, position, status, date_applied, deadline, notes):
    """
    Adds a new job application to the database
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (company, position, status, date_applied, deadline, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, position, status, date_applied, deadline, notes))

    conn.commit()
    conn.close()

# Delete function
def delete_application(app_id):
    """
    Deletes a job application by ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,)
    )

    conn.commit()
    conn.close()

# Update function
def update_application(app_id, company, position, status, date_applied, deadline, notes):
    """
    Updates an existing job application
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET company = ?,
            position = ?,
            status = ?,
            date_applied = ?,
            deadline = ?,
            notes = ?
        WHERE id = ?
    """, (company, position, status, date_applied, notes, deadline, app_id))

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
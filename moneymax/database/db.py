import sqlite3

def create_database():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('money_management.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create tables and define their structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            description TEXT,
            amount REAL
        )
    ''')

    # Commit the changes and close the connection when done
    conn.commit()
    conn.close()
import sqlite3

def create_user_database(username):
    user_db_name = f"./database/{username}.db"
    user_conn = sqlite3.connect(user_db_name)
    user_cursor = user_conn.cursor()

    user_cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date TEXT,
            tags TEXT
        )
    ''')

    user_conn.commit()
    user_conn.close()

def create_user_config(username):
    user_db_name = f"./database/{username}_config.db"
    user_conn = sqlite3.connect(user_db_name)
    user_cursor = user_conn.cursor()

    user_cursor.execute('''
                        CREATE TABLE IF NOT EXISTS config (
                            MONTH_YEAR TEXT,
                            CURRENT_TOTAL REAL,
                            CURRENT_SAVINGS REAL,
                            BUDGET REAL,
                            WANTS REAL,
                            NEEDS REAL,
                            SAVINGS REAL
                        )
                        ''')
    user_conn.commit()
    user_conn.close()
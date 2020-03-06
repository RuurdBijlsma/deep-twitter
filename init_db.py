import sqlite3


def init_db(db_name='tweets.db'):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets
                 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL
                  )
    """)
    return db, cursor

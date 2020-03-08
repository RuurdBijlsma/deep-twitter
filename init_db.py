import sqlite3


def clean_db(cursor):
    print("Drop tweets")
    cursor.execute("DROP TABLE IF EXISTS tweets")
    cursor.execute("DROP TABLE IF EXISTS metadata")
    cursor.execute("DROP INDEX IF EXISTS user_index;")


def init_db(db_name='data/tweets.db', clean=True):
    db = sqlite3.connect(db_name, check_same_thread=False)
    cursor = db.cursor()
    if clean:
        clean_db(cursor)
        db.commit()
    print("Create tweets")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets
                 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL
                  )
    """)
    print("Create metadata")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata
                 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    max_sentence_length INTEGER NOT NULL
                  )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS user_index on tweets(user)
    """)
    db.commit()
    return db, cursor

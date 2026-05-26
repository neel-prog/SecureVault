import sqlite3, os

APP_DIR = os.path.join(os.getenv("APPDATA"), "SecureVault")
os.makedirs(APP_DIR, exist_ok=True)

DB_FILE = os.path.join(APP_DIR, "vault.db")

def connect():
    return sqlite3.connect(DB_FILE)

def setup():
    conn = connect()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS master(password TEXT)")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vault(
        id INTEGER PRIMARY KEY,
        website TEXT,
        username TEXT,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()
import sqlite3

def get_db():
    conn = sqlite3.connect('todo.db')
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS last_reset (
            id INTEGER PRIMARY KEY,
            reset_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
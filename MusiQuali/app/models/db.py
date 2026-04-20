import sqlite3



def get_db():
    from app import app
    conn = sqlite3.connect(app.static_folder + '/data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table Playlists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Table Musics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT,
            duration INTEGER,
            path TEXT,
            playlist_id INTEGER,
            FOREIGN KEY (playlist_id) REFERENCES playlists (id)
        )
    ''')
    
    # Table Schedule Days (Start time per day)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_days (
            day_name TEXT PRIMARY KEY,
            start_time TEXT
        )
    ''')
    
    # Table Schedule Items (Tasks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_name TEXT,
            position INTEGER,
            title TEXT,
            artist TEXT,
            duration INTEGER,
            path TEXT,
            FOREIGN KEY (day_name) REFERENCES schedule_days (day_name)
        )
    ''')
    
    # Initialize default days
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day in days:
        cursor.execute('INSERT OR IGNORE INTO schedule_days (day_name, start_time) VALUES (?, ?)', (day, '08:00'))
        
    conn.commit()
    conn.close()
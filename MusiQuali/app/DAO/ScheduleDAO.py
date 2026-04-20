import sqlite3
from app.models.db import get_db



DB_NAME = "planning.db"



class ScheduleDAO:
    def init_db(self):
        conn = get_db()
        c = conn.cursor()
        # c.execute('CREATE TABLE IF NOT EXISTS playlist (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, name TEXT)')
        c.execute('''CREATE TABLE IF NOT EXISTS music (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        title TEXT, 
                        duration INTEGER, 
                        path TEXT
                        );''')
        c.execute('CREATE TABLE IF NOT EXISTS schedule_day (day_name TEXT PRIMARY KEY, start_time TEXT)')
        c.execute('''CREATE TABLE IF NOT EXISTS schedule_item (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        day_name TEXT, 
                        position INTEGER, 
                        title TEXT, 
                        artist TEXT, 
                        duration INTEGER, 
                        path TEXT,
                        FOREIGN KEY(day_name) REFERENCES schedule_day(day_name))''')
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            c.execute('INSERT OR IGNORE INTO schedule_day (day_name, start_time) VALUES (?, ?)', (day, "00:00"))
        conn.commit()
        conn.close()

    def get_start_time(self, day):
        conn = get_db()
        row = conn.execute('SELECT start_time FROM schedule_day WHERE day_name = ?', (day,)).fetchone()
        conn.close()
        return row['start_time'] if row else "00:00"

    def update_start_time(self, day, start_time):
        conn = get_db()
        conn.execute('UPDATE schedule_day SET start_time = ? WHERE day_name = ?', (start_time, day))
        conn.commit()
        conn.close()

    def get_items_by_day(self, day):
        conn = get_db()
        items = conn.execute('SELECT * FROM schedule_item WHERE day_name = ? ORDER BY position', (day,)).fetchall()
        conn.close()
        return items

    def clear_day_items(self, day):
        conn = get_db()
        conn.execute('DELETE FROM schedule_item WHERE day_name = ?', (day,))
        conn.commit()
        conn.close()

    def add_item(self, day, position, title, artist, duration, path):
        conn = get_db()
        conn.execute('INSERT INTO schedule_item (day_name, position, title, artist, duration, path) VALUES (?, ?, ?, ?, ?, ?)',
                     (day, position, title, artist, int(duration), path))
        conn.commit()
        conn.close()
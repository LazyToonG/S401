import sqlite3
from app import app
from app.models.Music import Music
import os

class MusicDAO:

    def __init__(self):
        
        self.db=app.static_folder +'/data/database.db'
        self._init_db()

    def _init_db(self):
        conn = self.get_connection()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS music (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                duration INTEGER, 
                path TEXT NOT NULL
            );
        """)

    def get_connection(self):
        conn = sqlite3.connect(os.path.join(app.static_folder, "data", "database.db"))
        conn.row_factory = sqlite3.Row
        return conn

    def get_all(self):
        conn = self.get_connection()
        rows = conn.execute(
            "SELECT id, title, path, duration FROM music"
        ).fetchall()
        conn.close()
        return [Music(row["id"], row["title"], row["path"], row["duration"]) for row in rows]

    def get_by_id(self, music_id):
        conn = self.get_connection()
        row = conn.execute(
            "SELECT id, title, path, duration FROM music WHERE id = ?",
            (music_id,)
        ).fetchone()
        conn.close()
        return Music(row["id"], row["title"], row["path"], row["duration"]) if row else None

    def create(self, title, path, duration):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO music (title, path, duration) VALUES (?, ?, ?)",
            (title, path, duration)
        )
        conn.commit()
        music_id = cur.lastrowid
        conn.close()

        return Music(music_id, title, path, duration)

    def delete(self, music_id):
        conn = self.get_connection()
        conn.execute("DELETE FROM music WHERE id = ?", (music_id,))
        conn.commit()
        conn.close()

    def get_musiques(self, order_by="title"):
        allowed = {
            "title": "title",
            "duration": "duration"
        }

        order_column = allowed.get(order_by, "title")

        conn = self.get_connection()
        rows = conn.execute(
            f"SELECT id, title, path, duration FROM music ORDER BY {order_column}"
        ).fetchall()
        conn.close()

        return [Music(row["id"], row["title"], row["path"], row["duration"]) for row in rows]

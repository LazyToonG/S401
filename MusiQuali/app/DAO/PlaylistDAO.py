import sqlite3
from app.models.Playliste import Playliste
import os
from app.models.db import get_db
from app import app
class PlaylisteDAO:

    def __init__(self):
        
        self.db=app.static_folder +'/data/database.db'
        self._init_db()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._getDbConnection()
        cursor = conn.cursor()
        
        table_exists = cursor.fetchone() is not None
        conn.execute("""
            CREATE TABLE IF NOT EXISTS playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                music_ids TEXT
            )
        """)
        conn.commit()

# verif si table exist
        cursor.execute(
            "SELECT 1 FROM playlist WHERE title = ?", ("annonces",)
            )

        if not table_exists:
            conn.execute("""

            INSERT INTO playlist (title, music_ids)
            VALUES ('annonces', NULL);

            """)

        conn.commit()
        conn.close()
        

    def _ids_to_str(self, ids):
        return "|".join(str(i) for i in ids)

    def _str_to_ids(self, data):
        return [int(i) for i in data.split("|")] if data else []

    def insert(self, playlist: Playliste):
        conn = self._getDbConnection()
        cur = conn.cursor()

        music_ids_str = self._ids_to_str(playlist.music_ids)

        if playlist.id is None:
            cur.execute(
                "INSERT INTO playlist (title, music_ids) VALUES (?, ?)",
                (playlist.title, music_ids_str)
            )
            playlist.id = cur.lastrowid
        else:
            cur.execute(
                "UPDATE playlist SET title=?, music_ids=? WHERE id=?",
                (playlist.title, music_ids_str, playlist.id)
            )

        conn.commit()
        conn.close()

    def get(self, playlist_id):
        conn = self._getDbConnection()
        row = conn.execute(
            "SELECT id, title, music_ids FROM playlist WHERE id=?",
            (playlist_id,)
        ).fetchone()
        conn.close()

        if not row:
            return None

        return Playliste(
            id=row[0],
            title=row[1],
            music_ids=self._str_to_ids(row[2])
        )

    def get_all(self):
        conn = self._getDbConnection()
        rows = conn.execute("SELECT * FROM playlist").fetchall()
        conn.close()

        return [
            Playliste(
                id=row[0],
                title=row[1],
                music_ids=self._str_to_ids(row[2])
            )
            for row in rows
        ]

    def delete(self, playlist_id): #appeler seulement apres avoir effacé les musiques
        conn = self._getDbConnection()
        conn.execute("DELETE FROM playlist WHERE id = ?", (playlist_id,))
        conn.commit()
        conn.close()
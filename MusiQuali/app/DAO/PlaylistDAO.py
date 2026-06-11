import sqlite3
from app.models.Playlist import Playlist
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

        # Création table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Playlist(
                idPlaylist INTEGER PRIMARY KEY AUTOINCREMENT,
                idUtilisateur INT NOT NULL DEFAULT 1,
                idPlanning INT default 1,
                title VARCHAR(100) NOT NULL,
                FOREIGN KEY(idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
                FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
            );
        """)

        # Ajout playlist "annonces" uniquement si elle n'existe pas
        cursor.execute("""
            SELECT 1 FROM Playlist WHERE title = ?
        """, ("annonces",))

        exists = cursor.fetchone() is not None

        # if not exists:
        #     conn.execute("""
        #         INSERT INTO Playlist (title)
        #         VALUES ('annonces');
        #     """)

        conn.commit()
        conn.close()
        

    def _ids_to_str(self, ids):
        return "|".join(str(i) for i in ids)

    def _str_to_ids(self, data):
        return [int(i) for i in data.split("|")] if data else []

    def insert(self, playlist: Playlist):
        conn = self._getDbConnection()
        cur = conn.cursor()


        if playlist.idPlaylist is None:
            cur.execute(
                "INSERT INTO Playlist (title, idUtilisateur, idPlanning) VALUES (?, ?, ?)",
                (playlist.title, playlist.idUtilisateur, playlist.idPlanning)
            )
            playlist.idPlaylist = cur.lastrowid
        else:
            cur.execute(
                "UPDATE Playlist SET title=? WHERE idPlaylist=?",
                (playlist.title,  playlist.idPlaylist)
            )

        conn.commit()
        conn.close()

    def get(self, playlist_id):
        conn = self._getDbConnection()

        row = conn.execute(
            "SELECT * FROM Playlist WHERE idPlaylist=?",
            (playlist_id,)
        ).fetchone()

        conn.close()

        if not row:
            return None

        return Playlist(
            idPlaylist=row["idPlaylist"],
            title=row["title"],
            idUtilisateur=row["idUtilisateur"],
            idPlanning=row["idPlanning"]
        )

    def get_all(self):
        conn = self._getDbConnection()
        rows = conn.execute("SELECT * FROM Playlist").fetchall()
        conn.close()

        return [
            Playlist(
                idPlaylist=row["idPlaylist"],
                title=row["title"],
                idUtilisateur=row["idUtilisateur"],
                idPlanning=row["idPlanning"]
            )
            for row in rows
        ]

    def delete(self, playlist_id): #appeler seulement apres avoir effacé les musiques
        conn = self._getDbConnection()
        conn.execute(
                "DELETE FROM Playlist WHERE idPlaylist = ?",
                (int(playlist_id),)
            )
        conn.commit()
        conn.close()
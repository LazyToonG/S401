import sqlite3
import os
from app import app

class RelationPlaylistMusicDAO:

    def __init__(self):
        self.db = app.static_folder + '/data/database.db'
        self._init_db()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._getDbConnection() #je veux que les doublon soient possibles.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS PlaylistMusique(
                INTEGER PRIMARY KEY AUTOINCREMENT, 
                idPlaylist INTEGER NOT NULL,
                idMusique  INTEGER NOT NULL,
                
                FOREIGN KEY (idPlaylist) REFERENCES Playlist(idPlaylist),
                FOREIGN KEY (idMusique)  REFERENCES Musique(idMusique)
            );
        """)
        conn.commit()
        conn.close()

    def add(self, idPlaylist, idMusique):
        """Ajoute une musique à une playlist."""
        conn = self._getDbConnection()
        try:
            conn.execute(
                "INSERT INTO PlaylistMusique (idPlaylist, idMusique) VALUES (?, ?)",
                (idPlaylist, idMusique)
            )
            conn.commit()
        finally:
            conn.close()

    def remove(self, idPlaylist, idMusique):
        """Retire une musique d'une playlist."""
        conn = self._getDbConnection()
        conn.execute(
            "DELETE FROM PlaylistMusique WHERE idPlaylist = ? AND idMusique = ?",
            (idPlaylist, idMusique)
        )
        conn.commit()
        conn.close()

    def get_musiques_by_playlist(self, idPlaylist):
        """Retourne la liste des idMusique pour une playlist donnée."""
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT idMusique FROM PlaylistMusique WHERE idPlaylist = ?",
            (idPlaylist,)
        ).fetchall()
        conn.close()
        return [row["idMusique"] for row in rows]

    def get_playlists_by_musique(self, idMusique):
        """Retourne la liste des idPlaylist contenant une musique donnée."""
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT idPlaylist FROM PlaylistMusique WHERE idMusique = ?",
            (idMusique,)
        ).fetchall()
        conn.close()
        return [row["idPlaylist"] for row in rows]

    def remove_all_from_playlist(self, idPlaylist):
        """Vide complètement une playlist (utile avant de la reconstruire)."""
        conn = self._getDbConnection()
        conn.execute(
            "DELETE FROM PlaylistMusique WHERE idPlaylist = ?",
            (idPlaylist,)
        )
        conn.commit()
        conn.close()
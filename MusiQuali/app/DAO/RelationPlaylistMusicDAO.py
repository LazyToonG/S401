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
                idCouple INTEGER PRIMARY KEY AUTOINCREMENT, 
                idPlaylist INTEGER NOT NULL,
                idMusique  INTEGER NOT NULL,
                position INTEGER,
                FOREIGN KEY (idPlaylist) REFERENCES Playlist(idPlaylist),
                FOREIGN KEY (idMusique)  REFERENCES Musique(idMusique)
            );

        """)
        conn.commit()
        conn.close()

    def add(self, idPlaylist, idMusique, position):
        """Ajoute une musique à une playlist. Si position non fournie, place en dernier."""
        conn = self._getDbConnection()
        try:
            if position is None:
                row = conn.execute(
                    "SELECT COALESCE(MAX(position), 0) + 1 AS next_pos FROM PlaylistMusique WHERE idPlaylist = ?",
                    (idPlaylist,)
                ).fetchone()
                position = row["next_pos"]
            conn.execute(
                "INSERT INTO PlaylistMusique (idPlaylist, idMusique, position) VALUES (?, ?, ?)",
                (idPlaylist, idMusique, position)
            )
            conn.commit()
        finally:
            conn.close()

    def remove(self, idCouple):
        """Retire une entrée de la playlist par son idCouple (supporte les doublons)."""
        conn = self._getDbConnection()
        conn.execute(
            "DELETE FROM PlaylistMusique WHERE idCouple = ?",
            (idCouple,)
        )
        conn.commit()
        conn.close()

    def get_musiques_by_playlist(self, idPlaylist):
        """Retourne idCouple, idMusique et position pour une playlist, triés par position."""
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT idCouple, idMusique, position FROM PlaylistMusique WHERE idPlaylist = ? ORDER BY position",
            (idPlaylist,)
        ).fetchall()
        conn.close()
        return [{"idCouple": row["idCouple"], "idMusique": row["idMusique"], "position": row["position"]} for row in rows]

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

    def update_position(self, idCouple, position):
        """Met à jour la position d'une entrée playlist-musique."""
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE PlaylistMusique SET position = ? WHERE idCouple = ?",
            (position, idCouple)
        )
        conn.commit()
        conn.close()
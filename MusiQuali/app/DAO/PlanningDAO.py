import sqlite3
from app.models.Planning import Planning
from app import app


class PlanningDAO:

    def __init__(self):

        self.db = app.static_folder + '/data/database.db'
        self._init_db()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._getDbConnection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Planning(
                idPlanning INTEGER PRIMARY KEY AUTOINCREMENT,
                idPlaylist INT,
                idMSG INT,
                StartTime DATETIME NOT NULL,
                idEntreprise INT NOT NULL DEFAULT 1,
                FOREIGN KEY(idPlaylist) REFERENCES Playlist(idPlaylist),
                FOREIGN KEY(idMSG) REFERENCES Musique(idMusique),
                FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
            );
        """)

        conn.commit()
        conn.close()

    def create(self, planning: Planning):
        conn = self._getDbConnection()
        cur = conn.cursor()

        if planning.idPlanning is None:
            cur.execute(
                "INSERT INTO Planning (idPlaylist, idMSG, StartTime, idEntreprise) VALUES (?, ?, ?, ?)",
                (planning.idPlaylist, planning.idMSG, planning.StartTime, planning.idEntreprise)
            )
            planning.idPlanning = cur.lastrowid
        else:
            cur.execute(
                "UPDATE Planning SET idPlaylist=?, idMSG=?, StartTime=?, idEntreprise=? WHERE idPlanning=?",
                (planning.idPlaylist, planning.idMSG, planning.StartTime,
                 planning.idEntreprise, planning.idPlanning)
            )

        conn.commit()
        conn.close()
        return planning

    def get(self, planning_id):
        conn = self._getDbConnection()

        row = conn.execute(
            "SELECT * FROM Planning WHERE idPlanning=?",
            (planning_id,)
        ).fetchone()

        conn.close()

        if not row:
            return None

        return Planning(
            idPlanning=row["idPlanning"],
            idPlaylist=row["idPlaylist"],
            idMSG=row["idMSG"],
            StartTime=row["StartTime"],
            idEntreprise=row["idEntreprise"]
        )

    def get_all(self, idEntreprise):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Planning WHERE idEntreprise=?",
            (idEntreprise,)
        ).fetchall()
        conn.close()

        return [
            Planning(
                idPlanning=row["idPlanning"],
                idPlaylist=row["idPlaylist"],
                idMSG=row["idMSG"],
                StartTime=row["StartTime"],
                idEntreprise=row["idEntreprise"]
            )
            for row in rows
        ]

    def delete(self, planning_id):
        conn = self._getDbConnection()
        conn.execute(
            "DELETE FROM Planning WHERE idPlanning = ?",
            (int(planning_id),)
        )
        conn.commit()
        conn.close()

    # -------------------- Requêtes d'export (MU.json / MSG.json) --------------------

    def get_message_slots(self, idEntreprise):
        """
        Retourne chaque créneau "message" planifié, avec le nom de fichier de la musique
        associée (jointure directe Planning.idMSG = Musique.idMusique).
        """
        conn = self._getDbConnection()
        rows = conn.execute("""
            SELECT pl.idPlanning, pl.StartTime, m.nomMusique
            FROM Planning pl
            JOIN Musique m ON pl.idMSG = m.idMusique
            WHERE pl.idEntreprise = ? AND pl.idMSG IS NOT NULL
            ORDER BY pl.StartTime
        """, (idEntreprise,)).fetchall()
        conn.close()

        return [
            {"idPlanning": row["idPlanning"], "StartTime": row["StartTime"], "nomMusique": row["nomMusique"]}
            for row in rows
        ]

    def get_playlist_slots(self, idEntreprise):
        """
        Retourne chaque créneau "playlist" planifié, avec la liste ordonnée (par position)
        des noms de fichiers des musiques qu'elle contient (jointure via PlaylistMusique).
        """
        conn = self._getDbConnection()
        slot_rows = conn.execute("""
            SELECT pl.idPlanning, pl.StartTime, pl.idPlaylist
            FROM Planning pl
            WHERE pl.idEntreprise = ? AND pl.idPlaylist IS NOT NULL
            ORDER BY pl.StartTime
        """, (idEntreprise,)).fetchall()

        slots = []
        for slot in slot_rows:
            track_rows = conn.execute("""
                SELECT m.nomMusique
                FROM PlaylistMusique pm
                JOIN Musique m ON pm.idMusique = m.idMusique
                WHERE pm.idPlaylist = ?
                ORDER BY pm.position
            """, (slot["idPlaylist"],)).fetchall()

            slots.append({
                "idPlanning": slot["idPlanning"],
                "StartTime": slot["StartTime"],
                "idPlaylist": slot["idPlaylist"],
                "musics": [t["nomMusique"] for t in track_rows]
            })

        conn.close()
        return slots
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

    def get_all(self, idEntreprise=1):
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

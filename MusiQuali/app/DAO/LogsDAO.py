import sqlite3
from datetime import datetime
from app import app
from app.models.Logs import Logs

class LogsSqliteDAO():

    def __init__(self):
        self.databasename = app.static_folder + '/data/database.db'
        self._initTable()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _initTable(self):
        """Crée la table logs si elle n’existe pas"""
        with self._getDbConnection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Logs(
                    idLogs INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomFichierLog VARCHAR(25) NOT NULL,
                    idLecteur INT NOT NULL default 1,
                    UNIQUE(nomFichierLog),
                    FOREIGN KEY(idLecteur) REFERENCES Lecteur(idLecteur)
                    );
            """)

    def _row_to_log(self, row):
        return Logs(
            idLogs=row["idLogs"],
            idLecteur=row["idLecteur"],
            nomFichierLog=row["nomFichierLog"],
        )

    # ------------------- GETTERS -------------------
    def get_all(self):
        with self._getDbConnection() as conn:
            cursor = conn.execute("SELECT * FROM Logs ORDER BY idLogs ASC")
            return [self._row_to_log(row) for row in cursor.fetchall()]

    def get_by_id(self, id):
        with self._getDbConnection() as conn:
            row = conn.execute("SELECT * FROM Logs WHERE idLogs=?", (id,)).fetchone()
            return self._row_to_log(row) if row else None

    def get_by_raspberry(self, id_rasp):
        with self._getDbConnection() as conn:
            cursor = conn.execute(
                "SELECT * FROM Logs WHERE idLecteur=? ORDER BY idLogs ASC", (id_rasp,)
            )
            return [self._row_to_log(row) for row in cursor.fetchall()]

    # def get_by_date(self, date_str):
    #     """Retourne tous les logs pour une date donnée (format 'YYYY-MM-DD')"""
    #     with self._connect() as conn:
    #         cursor = conn.execute(
    #             "SELECT * FROM Logs WHERE date LIKE ? ORDER BY idLogs ASC", (f"{date_str}%",)
    #         )
    #         return [self._row_to_log(row) for row in cursor.fetchall()]

    def get_latest(self):
        """Retourne le dernier log ajouté"""
        with self._getDbConnection() as conn:
            row = conn.execute("SELECT * FROM Logs ORDER BY idLogs DESC LIMIT 1").fetchone()
            return self._row_to_log(row) if row else None

    
    def insert(self, idLecteur, nomFichierLog):
        """Insère un nouveau log. date au format 'YYYY-MM-DD HH:MM:SS' ou maintenant par défaut"""
        # if date is None:
        #     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._getDbConnection() as conn:
            cursor = conn.execute(
                "INSERT INTO Logs (idLecteur, nomFichierLog) VALUES (?, ?)",
                (idLecteur, nomFichierLog)
            )
            return cursor.lastrowid
        
    def delete(self, id):
        """Supprime un log par son id"""
        with self._getDbConnection() as conn:
            conn.execute("DELETE FROM Logs WHERE idLogs=?", (id,))

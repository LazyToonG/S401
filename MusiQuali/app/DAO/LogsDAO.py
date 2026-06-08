import sqlite3
from datetime import datetime
from app.models.Logs import Logs

class LogsSqliteDAO():
    def __init__(self, idLogs, idLecteur, nomFichierLog):
        self.idLogs = idLogs
        self.idLecteur = idLecteur
        self.nomFichierLog = nomFichierLog

    def __repr__(self):
        return f"<Logs id={self.idLogs} idLecteur={self.idLecteur} nomFichierLog={self.nomFichierLog}>"

class LogsDAO:
    def __init__(self, nomFichierLog):
        self.db_path = nomFichierLog
        self._init_table()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # permet d’accéder aux colonnes par nom
        return conn

    def _init_table(self):
        """Crée la table logs si elle n’existe pas"""
        with self._connect() as conn:
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
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM Logs ORDER BY idLogs ASC")
            return [self._row_to_log(row) for row in cursor.fetchall()]

    def get_by_id(self, id):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM Logs WHERE idLogs=?", (id,)).fetchone()
            return self._row_to_log(row) if row else None

    def get_by_raspberry(self, id_rasp):
        with self._connect() as conn:
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
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM Logs ORDER BY idLogs DESC LIMIT 1").fetchone()
            return self._row_to_log(row) if row else None

    
    def insert(self, idLecteur, nomFichierLog):
        """Insère un nouveau log. date au format 'YYYY-MM-DD HH:MM:SS' ou maintenant par défaut"""
        # if date is None:
        #     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO Logs (idLecteur, nomFichierLog) VALUES (?, ?)",
                (idLecteur, nomFichierLog)
            )
            return cursor.lastrowid

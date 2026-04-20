import sqlite3
from datetime import datetime

class Logs:
    def __init__(self, id, idRaspberry, date, path):
        self.id = id
        self.idRaspberry = idRaspberry
        self.date = date
        self.path = path

    def __repr__(self):
        return f"<Logs id={self.id} idRaspberry={self.idRaspberry} date={self.date} path={self.path}>"

class LogsDAO:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_table()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # permet d’accéder aux colonnes par nom
        return conn

    def _init_table(self):
        """Crée la table logs si elle n’existe pas"""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    idRaspberry TEXT NOT NULL,
                    date TEXT NOT NULL,
                    path TEXT NOT NULL
                )
            """)

    def _row_to_log(self, row):
        return Logs(
            id=row["id"],
            idRaspberry=row["idRaspberry"],
            date=row["date"],
            path=row["path"]
        )

    # ------------------- GETTERS -------------------
    def get_all(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM logs ORDER BY date ASC")
            return [self._row_to_log(row) for row in cursor.fetchall()]

    def get_by_id(self, id):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM logs WHERE id=?", (id,)).fetchone()
            return self._row_to_log(row) if row else None

    def get_by_raspberry(self, id_rasp):
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM logs WHERE idRaspberry=? ORDER BY date ASC", (id_rasp,)
            )
            return [self._row_to_log(row) for row in cursor.fetchall()]

    def get_by_date(self, date_str):
        """Retourne tous les logs pour une date donnée (format 'YYYY-MM-DD')"""
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM logs WHERE date LIKE ? ORDER BY date ASC", (f"{date_str}%",)
            )
            return [self._row_to_log(row) for row in cursor.fetchall()]

    def get_latest(self):
        """Retourne le dernier log ajouté"""
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM logs ORDER BY date DESC LIMIT 1").fetchone()
            return self._row_to_log(row) if row else None

    
    def insert(self, idRaspberry, path, date=None):
        """Insère un nouveau log. date au format 'YYYY-MM-DD HH:MM:SS' ou maintenant par défaut"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO logs (idRaspberry, date, path) VALUES (?, ?, ?)",
                (idRaspberry, date, path)
            )
            return cursor.lastrowid

import sqlite3
from app import app
from app.models.Music import Music
import os

class MusicDAO():

    def __init__(self):
        
        self.db=app.static_folder +'/data/database.db'
        self._init_db()

    def _init_db(self):
        conn = self.get_connection()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Musique(
                idMusique INTEGER PRIMARY KEY AUTOINCREMENT,
                nomMusique VARCHAR(50) NOT NULL,
                duree INT NOT NULL,
                idEntreprise INT NOT NULL default 1,
                FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
                );
        """)
        conn.commit()
        conn.close()

    def get_connection(self):
        conn = sqlite3.connect(os.path.join(app.static_folder, "data", "database.db"))
        conn.row_factory = sqlite3.Row
        return conn

    def get_all(self):
        conn = self.get_connection()
        rows = conn.execute(
            "SELECT idMusique, nomMusique, duree, idEntreprise FROM Musique"
        ).fetchall()
        conn.close()
        return [Music(row["idMusique"], row["nomMusique"], row["duree"], row["idEntreprise"]) for row in rows]

    def get_by_id(self, idMusique):
        conn = self.get_connection()
        row = conn.execute(
            "SELECT idMusique, nomMusique, duree, idEntreprise FROM Musique WHERE idMusique = ?",
            (idMusique,)
        ).fetchone()
        conn.close()
        return Music(row["idMusique"], row["nomMusique"], row["duree"], row["idEntreprise"]) if row else None

    def create(self, nomMusique, duree, idEntreprise):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Musique (nomMusique, duree, idEntreprise) VALUES (?, ?, ?)",
            (nomMusique, duree, idEntreprise)
        )
        conn.commit()
        idMusique = cur.lastrowid
        conn.close()

        return Music(idMusique, nomMusique, duree, idEntreprise)

    def delete(self, idMusique):
        conn = self.get_connection()
        conn.execute("DELETE FROM Musique WHERE idMusique = ?", (idMusique,))
        conn.commit()
        conn.close()

    def get_musiques(self, order_by="nomMusique"):
        allowed = {
            "nomMusique": "nomMusique",
            "duree": "duree"
        }

        order_column = allowed.get(order_by, "nomMusique")

        conn = self.get_connection()
        rows = conn.execute(
            f"SELECT idMusique, nomMusique, duree, idEntreprise FROM Musique ORDER BY {order_column}"
        ).fetchall()
        conn.close()

        return [Music(row["idMusique"], row["nomMusique"], row["duree"], row["idEntreprise"]) for row in rows]

import sqlite3, os
from app import app
from app.models.Entreprise import Entreprise

class EntrepriseSqliteDAO():

    def __init__(self):
        self.databasename = app.static_folder + '/data/database.db'
        self._initTable()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _initTable(self):
        conn = self._getDbConnection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Entreprise(
                idEntreprise INTEGER PRIMARY KEY AUTOINCREMENT,
                nomEntreprise VARCHAR(50) NOT NULL DEFAULT 'testEntreprise',
                UNIQUE(nomEntreprise)
            );
        """)
        # entreprise par défaut
        conn.execute("""
            INSERT OR IGNORE INTO Entreprise (idEntreprise, nomEntreprise)
            VALUES (5, 'testEntreprise');
        """)
        conn.commit()
        conn.close()

    def createEntreprise(self, nomEntreprise):
        conn = self._getDbConnection()
        try:
            conn.execute(
                "INSERT INTO Entreprise (nomEntreprise) VALUES (?)",
                (nomEntreprise,)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("ERROR create Entreprise:", e)
            return False
        finally:
            conn.close()

    def findAll(self):
        conn = self._getDbConnection()
        rows = conn.execute("SELECT * FROM Entreprise").fetchall()
        conn.close()

        return [
            Entreprise(row["idEntreprise"], row["nomEntreprise"])
            for row in rows
        ]
    
    def findById(self, idEntreprise):
        conn = self._getDbConnection()
        row = conn.execute(
            "SELECT * FROM Entreprise WHERE idEntreprise = ?",
            (idEntreprise,)
        ).fetchone()
        conn.close()

        if row:
            return Entreprise(row["idEntreprise"], row["nomEntreprise"])
        return None
    
    def findByName(self, nomEntreprise):
        conn = self._getDbConnection()
        row = conn.execute(
            "SELECT * FROM Entreprise WHERE nomEntreprise = ?",
            (nomEntreprise,)
        ).fetchone()
        conn.close()

        if row:
            return Entreprise(row["idEntreprise"], row["nomEntreprise"])
        return None
    
    def delete(self, idEntreprise):
        conn = self._getDbConnection()
        try:
            conn.execute(
                "DELETE FROM Entreprise WHERE idEntreprise = ?",
                (idEntreprise,)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("ERROR delete Entreprise:", e)
            return False
        finally:
            conn.close()
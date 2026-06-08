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
        conn.commit()
        conn.close()
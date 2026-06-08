import sqlite3
from app import app
from app.models.Message import Message

class MessageSqliteDAO():

	def __init__(self):
		self.databasename = app.static_folder + '/data/database.db'
		self._initTable()
		
	def _getDbConnection(self):
		""" connect the database and returns the connection object """
		""" connection à la base de données. Retourne l'objet connection """
		conn = sqlite3.connect(self.databasename)
		conn.row_factory = sqlite3.Row
		return conn
	
	def _initTable(self):
		conn = self._getDbConnection()
		conn.execute('''
			CREATE TABLE IF NOT EXISTS Message(
                idMessage INTEGER PRIMARY KEY AUTOINCREMENT,
                nomFichierMessage VARCHAR(100) NOT NULL default 'tesmessage',
                duree INT NOT NULL default 0,
                idEntreprise INT NOT NULL default 1,
                idPlanning INT,
                FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise),
                FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
                );

		''')
		conn.commit()
		conn.close()
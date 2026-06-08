import sqlite3
from app import app
from app.models.Ajouter import Ajouter


class AjouterSqliteDAO():

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
			CREATE TABLE IF NOT EXISTS Ajouter(
                idMusique INT,
                idPlaylist INT,
                PRIMARY KEY(idMusique, idPlaylist),
                FOREIGN KEY(idMusique) REFERENCES Musique(idMusique),
                FOREIGN KEY(idPlaylist) REFERENCES Playlist(idPlaylist)
                );
		''')
		conn.commit()
		conn.close()
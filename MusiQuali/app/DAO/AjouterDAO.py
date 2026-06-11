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

	def getMusicIdsByPlaylist(self, idPlaylist):
		conn = self._getDbConnection()
		rows = conn.execute(
			"SELECT idMusique FROM Ajouter WHERE idPlaylist = ?",
			(idPlaylist,)
		).fetchall()
		conn.close()

		return [r["idMusique"] for r in rows]
	
	def add_music_to_playlist(self, idPlaylist, idMusique):
		conn = self._getDbConnection()
		conn.execute(
			"INSERT INTO Ajouter (idMusique, idPlaylist) VALUES (?, ?)",
			(idMusique, idPlaylist)
		)
		conn.commit()
		conn.close()
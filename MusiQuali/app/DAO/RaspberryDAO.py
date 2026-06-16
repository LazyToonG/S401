import sqlite3, os, subprocess
from app import app
from app.models.Raspberry import Raspberry

class RaspberrySqliteDAO():

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
			CREATE TABLE IF NOT EXISTS Lecteur(
				idLecteur INTEGER PRIMARY KEY AUTOINCREMENT,
				ip VARCHAR(50) NOT NULL,
				nomLecteur VARCHAR(50) NOT NULL,
				idEntreprise INT NOT NULL DEFAULT 1,
				UNIQUE(ip),
				FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
				);
		''')
		conn.commit()
		conn.close()

	#tentative supp table inutile dans la db
	# def _initTable(self):
	# 	conn = self._getDbConnection()

	# 	conn.execute("DROP TABLE IF EXISTS playlist;")
	# 	conn.execute("DROP TABLE IF EXISTS music;")
	# 	conn.execute("DROP TABLE IF EXISTS raspberry;")
	# 	conn.execute("DROP TABLE IF EXISTS users;")

	# 	conn.commit()
	# 	conn.close()

	def findAll(self):
		""" trouve tous les raspberry """
		conn = self._getDbConnection()
		raspberry = conn.execute('SELECT * FROM Lecteur').fetchall()
		raspberry_instances = list()
		for r in raspberry:
			# Ici on crée l'objet Raspberry avec les colonnes de la DB
			raspberry_instances.append(
				Raspberry(r["idLecteur"], r["nomLecteur"], r["ip"])
			)
		conn.close()
		return raspberry_instances
	
	def createRasp(self, nom, ip):
		"""Rajoute un raspberry dans la base de données"""
		conn = self._getDbConnection()
		try:
			conn.execute(
				"INSERT INTO Lecteur (nomLecteur, ip, idEntreprise) VALUES (?, ?, ?)",
				(nom, ip, 1)
			)
			conn.commit()
			return True
		except Exception as e:
			conn.rollback()
			print("ERROR createRasp:", e)
			return False
		finally:
			conn.close()

	def deleteRasp(self, idLecteur):
		"""Supprime un raspberry de la base dedonnées"""
		conn = self._getDbConnection()
		try:
			conn.execute(
				"DELETE FROM Lecteur WHERE idLecteur = :idLecteur",
				{"idLecteur":idLecteur}
			)
			conn.commit()
			return True
		except Exception:
			return False
		finally:
			conn.close() 

	def findById(self, idLecteur):
		"""Trouve une raspberry par son id"""
		conn = self._getDbConnection()
		r = conn.execute(
			"SELECT * FROM Lecteur WHERE idLecteur = ?",
			(idLecteur,)
		).fetchone()
		conn.close()
		print("rrrrrrr_dao :",r)
		if r:
			return r
		else:
			return None

	def findByIp(self, ip):
		"""Trouve une raspberry par son ip"""
		conn = self._getDbConnection()
		r = conn.execute(
			"SELECT * FROM Lecteur WHERE ip = ?",
			(ip,)
		).fetchone()
		conn.close()
		print("rrrrrrr_dao :",r)
		if r:
			return r["ip"]
		else:
			return None
	
	def findByNom(self, nomLecteur):
		"""Trouve une raspberry par son nom"""
		conn = self._getDbConnection()
		r = conn.execute(
			"SELECT * FROM Lecteur WHERE nomLecteur = ?",
			(nomLecteur,)
		).fetchone()
		conn.close()
		print("rrrrrrr_dao_nom :",r)
		if r:
			return r["nomLecteur"]
		else:
			return None
		

	def recherche(self, query):
		conn = self._getDbConnection()
        
        # On prépare le terme de recherche une seule fois
		search_term = f"{query}%"
        
        # La requête cherche dans nomLecteur OU dans ipRasp !
		rows = conn.execute(
            """
            SELECT * FROM Lecteur 
            WHERE nomLecteur LIKE ? OR ipRasp LIKE ? 
            ORDER BY nomLecteur ASC
            """,
            (search_term, search_term) # On donne le terme deux fois pour les deux '?'
        ).fetchall()
		
		conn.close()
		
		if not rows:
			return [] # On renvoie une liste vide si rien n'est trouvé

		return [Raspberry(r["idRasp"], r["nom"], r["ipRasp"]) for r in rows]
	

	def triASC(self):
		conn = self._getDbConnection()
		rows = conn.execute("SELECT * FROM Lecteur ORDER BY nomLecteur ASC").fetchall()
		conn.close()
		if not rows:
			return []
		return [Raspberry(r["idRasp"], r["nom"], r["ipRasp"]) for r in rows]
	
	def triDESC(self):
		conn = self._getDbConn
		rows = conn.execute("SELECT * FROM Lecteur ORDER BY nomLecteur DESC").fetchall()
		conn.close()
		if not rows:
			return []
		return [Raspberry(r["idRasp"], r["nom"], r["ipRasp"]) for r in rows]
	
	def triIP(self):
		conn = self._getDbConnection()
        # Trie par ordre alphabétique sur l'adresse IP
		rows = conn.execute("SELECT * FROM Lecteur ORDER BY ipRasp ASC").fetchall()
		conn.close()
		if not rows:
			return []
		return [Raspberry(r["idRasp"], r["nom"], r["ipRasp"]) for r in rows]

	# def VerifieShell(self):
	# 	raspberrys = self.findAll()
	# 	try:
	# 		for r in raspberrys:
	# 			subprocess.run(["ssh", r["nom"]+"@"+r["ipRasp"], "cd /"])
	# 			subprocess.run(["scp", "-v", app.static_folder + '/fichierDefaut/initialisationRaspberry', r["nom"]+"@"+r["ipRasp"]+":/home/"+r["nom"]+"/Music/"])
	# 			subprocess.run(["ssh", r["nom"]+"@"+r["ipRasp"], "chmod +x /home/"+r["nom"]+"/Music/initialisationRaspberry"])
	# 			subprocess.run(["ssh", r["nom"]+"@"+r["ipRasp"], "sudo /home/"+r["nom"]+"/Music/initialisationRaspberry.sh"])
	# 	except subprocess.CalledProcessError as e:
    #         print(f"Erreur sur {r['nom']} : {e}")
    #         return False
		
	# def verifieShell(self):
	# 	raspberrys = self.findAll()

	# 	for r in raspberrys:
	# 		host = f"{r.nom}@{r.ipRasp}"

	# 		try:
	# 			# subprocess.run(["ping", "-c", "1", r.ipRasp], check=True, timeout=5)

	# 			# # subprocess.run(["ssh", host, "cd /"], check=True, timeout=15)
	# 			subprocess.run(["scp", "-v", 'app/static/fichierDefaut/initialisationRaspberry', f"{host}:/home/{r.nom}/Music/"], check=True, timeout=30)

	# 			# # subprocess.run(["ssh", host, f"chmod +x /home/{r.nom}/Music/initialisationRaspberry"], check=True, timeout=15)
	# 			# # subprocess.run(["ssh", host, f"sudo /home/{r.nom}/Music/initialisationRaspberry.sh"], check=True, timeout=60)

	# 		except subprocess.CalledProcessError as e:
	# 			print(f"Erreur sur {host} : {e}")
	# 			return False
	# 		except subprocess.TimeoutExpired:
	# 			print(f"Timeout sur {host}")
	# 			return False

	# 	return True


# rdao = RaspberrySqliteDAO()

# class RaspberryVerifieChemin():
	
# 	def __init__(self, chemin):
# 		self.chemin = chemin
# 		self.estAJour()

# 	def estAJour(self):
# 		raspberrys = rdao.findAll()

# 		fichier = self.chemin
# 		# Stocke le temps de dernière modification
# 		dernier_time = os.path.getmtime(fichier)

# 		# Plus tard
# 		nouveau_time = os.path.getmtime(fichier)

# 		if nouveau_time != dernier_time:
# 			for r in raspberrys:
# 				subprocess.run(["scp", "-v", fichier, r["nom"]+"@"+r["ipRasp"]+":/home/"+r["nom"]+"/Music/"])

# class RaspberryVerifieChemin():
#     def __init__(self, chemin):
#         self.chemin = chemin
#         self.dernier_time = os.path.getmtime(chemin)

#     def estAJour(self):
#         nouveau_time = os.path.getmtime(self.chemin)
#         if nouveau_time != self.dernier_time:
#             self.dernier_time = nouveau_time
#             raspberrys = rdao.findAll()
#             for r in raspberrys:
#                 host = f"{r.nom}@{r.ipRasp}"
#                 subprocess.run(["scp", "-v", self.chemin, f"{host}:/home/{r.nom}/Music/"])




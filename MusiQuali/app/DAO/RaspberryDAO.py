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
			CREATE TABLE IF NOT EXISTS raspberry (
			    idRasp INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL DEFAULT 'raspberry',
				ipRasp TEXT NOT NULL
			)
		''')
		conn.commit()
		conn.close()

	def findAll(self):
		""" trouve tous les raspberry """
		conn = self._getDbConnection()
		raspberry = conn.execute('SELECT * FROM raspberry').fetchall()
		raspberry_instances = list()
		for r in raspberry:
			# Ici on crée l'objet Raspberry avec les colonnes de la DB
			raspberry_instances.append(
				Raspberry(r["idRasp"], r["nom"], r["ipRasp"])
			)
		conn.close()
		return raspberry_instances
	
	def createRasp(self, nom, ipRasp):
		conn = self._getDbConnection()
		try:
			conn.execute(
				"INSERT INTO raspberry (nom, ipRasp) VALUES (?, ?)",
				(nom, ipRasp)
			)
			conn.commit()
			return True
		except Exception as e:
			conn.rollback()
			print("ERROR createRasp:", e)
			return False
		finally:
			conn.close()

	def deleteRasp(self, idRasp):
		conn = self._getDbConnection()
		try:
			conn.execute(
				"DELETE FROM raspberry WHERE idRasp = :idRasp",
				{"idRasp":idRasp}
			)
			conn.commit()
			return True
		except Exception:
			return False
		finally:
			conn.close() 

	def findByIp(self, idRasp):
		conn = self._getDbConnection()
		r = conn.execute(
			"SELECT * FROM raspberry WHERE idRasp = ?",
			(idRasp,)
		).fetchone()
		conn.close()
		print("rrrrrrr_dao :",r)
		if r:
			return r["ipRasp"]
		else:
			return None
	
	def findByNom(self, idRasp):
		conn = self._getDbConnection()
		r = conn.execute(
			"SELECT * FROM raspberry WHERE idRasp = ?",
			(idRasp,)
		).fetchone()
		conn.close()
		print("rrrrrrr_dao_nom :",r)
		if r:
			return r["nom"]
		else:
			return None

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




import sqlite3, bcrypt
from app import app
from app.models.User import User

class UserSqliteDAO():

    def __init__(self):
        self.databasename = app.static_folder + '/data/database.db'
        self._initTable()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _initTable(self):
        

        conn = self._getDbConnection()
        cursor = conn.cursor()
        # verif si table exist
        cursor.execute("""
            SELECT 1
            FROM sqlite_master
            WHERE type='table' AND name='Users';
            """)
        table_exists = cursor.fetchone() is not None

            # rajouter not null a mail et trouver une soluce
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                idUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(15) NOT NULL,
                mail VARCHAR(50),
                idEntreprise INT NOT NULL default 1,
                UNIQUE(username),
                UNIQUE(mail),
                FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
                );
            """)

            # insert admin si table vient d'etre crée
        if not table_exists:
            self.createUser("admin", "admin", "admin", "admin@musiquali.com")

        conn.commit()
        conn.close()

        #ainsi, meme si on lance une bd vide on à un admin, mais que quand la table est crée donc que 1 fois

    def createUser(self, username, password, role, mail):
        conn = self._getDbConnection()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            conn.execute(
                "INSERT INTO Users(username, password, role, mail) VALUES (?,?,?,?)",
                (username, hashed, role, mail)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def getByUsername(self, username):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return User(**dict(user)) if user else None
    
    def getByEmail(self, mail):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Users WHERE mail = ?", (mail,)
        ).fetchone()
        conn.close()
        return User(**dict(user)) if user else None

    def verifyUser(self, username, password):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user is None:
            return None
        
        hashed = user["password"]
        
        # SÉCURITÉ : Si SQLite renvoie un texte normal (str), on le convertit en octets (bytes)
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
            
        if bcrypt.checkpw(password.encode('utf-8'), hashed):
            return User(**dict(user))
        return None
    
    def recherche(self, query):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users WHERE username LIKE ? ORDER BY username ASC",
            (f"{query}%",)
        ).fetchall()
        conn.close()
        
        if not rows: 
            return [] # On renvoie une liste vide au lieu de None !
            
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    def triASC(self):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users ORDER BY username ASC"
        ).fetchall()
        conn.close()
        if not rows: # S'il n'y a aucune selection correspondante
            return None
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    def triDESC(self):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users ORDER BY username DESC"
        ).fetchall()
        conn.close()
        if not rows: # S'il n'y a aucune selection correspondante
            return None
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    def triRole(self):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users ORDER BY role ASC"
        ).fetchall()
        conn.close()
        if not rows: # S'il n'y a aucune selection correspondante
            return None
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    
    def setUsername(self, username, new_username):
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Users SET username = ? WHERE username = ?",
            (new_username, username)
        )
        conn.commit()
        conn.close()

    def setEmail(self, username, new_mail):
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Users SET mail = ? WHERE username = ?",
            (new_mail, username)
        )
        conn.commit()
        conn.close()

    def setPassword(self, username, new_password):
        conn = self._getDbConnection()
        
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        conn.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed, username))
        conn.commit()
        conn.close()

    def setRole(self, username, new_role):
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Users SET role = ? WHERE username = ?",
            (new_role, username)
        )
        conn.commit()
        conn.close()

    def findAll(self):
        conn = self._getDbConnection()
        users = conn.execute('SELECT * FROM Users').fetchall()
        conn.close()
        return [User(**dict(u)) for u in users]

    def deleteByUsername(self, username):
        conn = self._getDbConnection()
        conn.execute("DELETE FROM Users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True

    

        




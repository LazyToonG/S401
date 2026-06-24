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

        # Création table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                idUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(15) NOT NULL,
                mail VARCHAR(50) NOT NULL,
                idEntreprise INT NOT NULL DEFAULT 1,
                UNIQUE(username, idEntreprise),
                UNIQUE(mail, idEntreprise),
                FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
            );
        """)

        # 1. Vérifier si un admin existe déjà
        cursor.execute("""
            SELECT 1 FROM Users WHERE role = 'admin' LIMIT 1;
        """)
        admin_exists = cursor.fetchone() is not None

        # Créer admin uniquement s’il n’existe pas (Corrigé : "admin" au lieu de "modo")
        if not admin_exists:
            self.createUser("admin", "admin", "admin", "admin@musiquali.com", 100)

        # 2. Vérifier si un modo existe déjà
        cursor.execute("""
            SELECT 1 FROM Users WHERE role = 'modo' LIMIT 1;
        """)
        modo_exists = cursor.fetchone() is not None

        # Créer modérateur uniquement s’il n’existe pas (Corrigé : le commentaire)
        if not modo_exists:
            self.createUser("modo", "modo", "modo", "modo@musiquali.com", 100)

        conn.commit()
        conn.close()

        #ainsi, meme si on lance une bd vide on à un admin, mais que quand la table est crée donc que 1 fois

    def createUser(self, username, password, role, mail, idEntreprise):
        conn = self._getDbConnection()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            conn.execute(
                "INSERT INTO Users(username, password, role, mail, idEntreprise) VALUES (?,?,?,?,?)",
                (username, hashed, role, mail, idEntreprise)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def getByUsername(self, username, idEntreprise):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Users WHERE username = ? AND idEntreprise = ?", (username, idEntreprise)
        ).fetchone()
        conn.close()
        return User(**dict(user)) if user else None
    
    def getByEmail(self, mail, idEntreprise=None):
        conn = self._getDbConnection()
        if idEntreprise:
            user = conn.execute(
                "SELECT * FROM Users WHERE mail = ? AND idEntreprise = ?",
                (mail, idEntreprise)
            ).fetchone()
        else:
            user = conn.execute(
                "SELECT * FROM Users WHERE mail = ?",
                (mail,)
            ).fetchone()
        conn.close()
        return User(**dict(user)) if user else None

    def verifyUser(self, username, password): #Keske je fais pour la vérif ;-;
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
    
    def recherche(self, query, idEntreprise):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users WHERE username LIKE ? AND idEntreprise = ? ORDER BY username ASC",
            (f"{query}%", idEntreprise)
        ).fetchall()
        conn.close()
        
        if not rows: 
            return [] # On renvoie une liste vide au lieu de None !
            
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    def triASC(self, idEntreprise):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users WHERE idEntreprise = ? ORDER BY username ASC", (idEntreprise,)
        ).fetchall()
        conn.close()
        if not rows: # S'il n'y a aucune selection correspondante
            return None
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    def triDESC(self, idEntreprise):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users WHERE idEntreprise = ? ORDER BY username DESC", (idEntreprise,)
        ).fetchall()
        conn.close()
        if not rows: # S'il n'y a aucune selection correspondante
            return None
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    def triRole(self, idEntreprise):
        conn = self._getDbConnection()
        rows = conn.execute(
            "SELECT * FROM Users WHERE idEntreprise = ? ORDER BY role ASC", (idEntreprise,)
        ).fetchall()
        conn.close()
        if not rows: # S'il n'y a aucune selection correspondante
            return None
        return [User(r["idUtilisateur"], r["username"], r["password"], r["role"], r["mail"], r["idEntreprise"]) for r in rows]
    
    
    def setUsername(self, username, new_username, idEntreprise):
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Users SET username = ? WHERE username = ? AND idEntreprise = ?",
            (new_username, username, idEntreprise)
        )
        conn.commit()
        conn.close()

    def setEmail(self, username, new_mail, idEntreprise):
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Users SET mail = ? WHERE username = ? AND idEntreprise = ?",
            (new_mail, username, idEntreprise)
        )
        conn.commit()
        conn.close()

    def setPassword(self, username, new_password, idEntreprise):
        conn = self._getDbConnection()
        
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        conn.execute("UPDATE Users SET password = ? WHERE username = ? AND idEntreprise = ?", (hashed, username, idEntreprise))
        conn.commit()
        conn.close()

    def setRole(self, username, new_role, idEntreprise):
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Users SET role = ? WHERE username = ? AND idEntreprise = ?",
            (new_role, username, idEntreprise)
        )
        conn.commit()
        conn.close()

    def findAll(self, idEntreprise):
        conn = self._getDbConnection()
        users = conn.execute('SELECT * FROM Users WHERE idEntreprise = ?', (idEntreprise,)
        ).fetchall()
        conn.close()
        return [User(**dict(u)) for u in users]
    
    def findAdminByEntreprise(self, idEntreprise):
        conn = self._getDbConnection()
        row = conn.execute(
            "SELECT * FROM Users WHERE role = 'admin' AND idEntreprise = ? LIMIT 1",
            (idEntreprise,)
        ).fetchone()
        conn.close()
        return User(**dict(row)) if row else None

    def deleteByUsername(self, username, idEntreprise):
        conn = self._getDbConnection()
        conn.execute("DELETE FROM Users WHERE username = ? AND idEntreprise = ?", (username, idEntreprise))
        conn.commit()
        conn.close()
        return True

    def deleteByIdEntreprise(self, idEntreprise):
        conn = self._getDbConnection()
        conn.execute("DELETE FROM Users WHERE idEntreprise = ?", (idEntreprise,))
        conn.commit()
        conn.close()
        return True

    

        




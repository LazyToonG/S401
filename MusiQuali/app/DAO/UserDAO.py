import sqlite3, bcrypt
from app import app
from app.models.User import User
from app.DAO.UserDAOInterface import UserDAOInterface

class UserSqliteDAO(UserDAOInterface):

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
                idEntreprise INT NOT NULL DEFAULT 1,
                UNIQUE(mail),
                FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
                );
            """)

            # insert admin si table vient d'etre crée
        if not table_exists:
            self.createUser("admin", "admin", "admin")

        conn.commit()
        conn.close()

        #ainsi, meme si on lance une bd vide on à un admin, mais que quand la table est crée donc que 1 fois

    def createUser(self, username, password, role):
        conn = self._getDbConnection()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            conn.execute(
                "INSERT INTO Users(username, password, role) VALUES (?,?,?)",
                (username, hashed, role)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def findByUsername(self, username):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return User(dict(user)) if user else None

    def verifyUser(self, username, password):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user is None:
            return None
        
        hashed = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), hashed):
            return User(dict(user))
        return None

    def findAll(self):
        conn = self._getDbConnection()
        users = conn.execute('SELECT * FROM Users').fetchall()
        conn.close()
        return [User(dict(u)) for u in users]

    def deleteByUsername(self, username):
        conn = self._getDbConnection()
        conn.execute("DELETE FROM Users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True

    

        




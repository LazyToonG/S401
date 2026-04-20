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
            WHERE type='table' AND name='users';
            """)
        table_exists = cursor.fetchone() is not None

            
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
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
                "INSERT INTO users(username, password, role) VALUES (?,?,?)",
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
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return User(dict(user)) if user else None

    def verifyUser(self, username, password):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
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
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [User(dict(u)) for u in users]

    def deleteByUsername(self, username):
        conn = self._getDbConnection()
        conn.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True

    

        




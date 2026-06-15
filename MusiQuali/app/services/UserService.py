from app.DAO.UserDAO import UserSqliteDAO as UserDAO

class UserService():
    def __init__(self):
        self.udao = UserDAO()

    def getUserByUsername(self, username):
        res = self.udao.getByUsername(username)
        if type(res) is not list:
            res = [res]
        return res
    
    def setUsername(self, username, mail, new_username):
        return self.udao.setUsername(username, mail, new_username)
    
    def setEmail(self, username, mail, new_mail):
        return self.udao.setRole(username, mail, new_mail)
    
    def setPassword(self, username, mail, new_password):
        return self.udao.setRole(username, mail, new_password)
    
    def setRole(self, username, mail, new_role):
        return self.udao.setRole(username, mail, new_role)

    def getUsers(self):
        return self.udao.findAll()
    
    def recherche(self, query):
        return self.udao.recherche(query)
    
    def triASC(self):
        return self.udao.triASC()
    
    def triDESC(self):
        return self.udao.triDESC()
    
    def triRole(self):
        return self.udao.triRole()
    
    def signin(self, username, password, role, mail):
        return self.udao.createUser(username, password, role, mail)

    def login(self, username, password):
        return self.udao.verifyUser(username, password)
    
    def deleteUser(self, username):
        return self.udao.deleteByUsername(username)
    

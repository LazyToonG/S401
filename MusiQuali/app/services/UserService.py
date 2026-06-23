from app.DAO.UserDAO import UserSqliteDAO as UserDAO

class UserService():
    def __init__(self):
        self.udao = UserDAO()

    def getUserByUsername(self, username, idEntreprise):
        res = self.udao.getByUsername(username, idEntreprise)
        if type(res) is not list:
            res = [res]
        return res

    def getUserByEmail(self, mail, idEntreprise):
        return self.udao.getByEmail(mail, idEntreprise)
    
    def setUsername(self, username, new_username, idEntreprise):
        return self.udao.setUsername(username, new_username, idEntreprise)
    
    def setEmail(self, username, new_mail, idEntreprise):
        return self.udao.setEmail(username, new_mail, idEntreprise)
    
    def setPassword(self, username, new_password, idEntreprise):
        return self.udao.setPassword(username, new_password, idEntreprise)
    
    def setRole(self, username, new_role, idEntreprise):
        return self.udao.setRole(username, new_role, idEntreprise)

    def getUsers(self, idEntreprise):
        return self.udao.findAll(idEntreprise)
    
    def recherche(self, query, idEntreprise):
        return self.udao.recherche(query, idEntreprise)
    
    def triASC(self, idEntreprise):
        return self.udao.triASC(idEntreprise)
    
    def triDESC(self, idEntreprise):
        return self.udao.triDESC(idEntreprise)
    
    def triRole(self, idEntreprise):
        return self.udao.triRole(idEntreprise)
    
    def signin(self, username, password, role, mail, idEntreprise):
        return self.udao.createUser(username, password, role, mail, idEntreprise)

    def login(self, username, password):
        return self.udao.verifyUser(username, password)
    
    def deleteUser(self, username, idEntreprise):
        return self.udao.deleteByUsername(username, idEntreprise)
    
    def deleteUserIdentreprise(self, idEntreprise):
        return self.udao.deleteByIdEntreprise(idEntreprise)

    def getAdminByEntreprise(self, idEntreprise):
        return self.udao.findAdminByEntreprise(idEntreprise)
    

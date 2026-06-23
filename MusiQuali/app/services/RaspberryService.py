from app.DAO.RaspberryDAO import RaspberrySqliteDAO as RaspberryDAO
import subprocess, ipaddress, time
from flask import render_template, request, redirect, url_for, flash


rd=RaspberryDAO()
import time, subprocess

class RaspberryService():
    def __init__(self):
        self.rdao = RaspberryDAO()

    def montreToutRasp(self, idEntreprise):
        return self.rdao.findAll(idEntreprise)

    def montreToutRaspGlobal(self):
        return self.rdao.findAllGlobal()
    
    def ajoutR(self, identifiant, ipRasp, idEntreprise):
        return self.rdao.createRasp(identifiant, ipRasp, idEntreprise)
    
    # def selectRIp(self, ipRasp):
    #     r = self.rdao.findByIp(ipRasp)
    #     if r:
    #         return r  # retourne une string
    #     return None

    # def selectRNom(self, nom):
    #     r = self.rdao.findByNom(nom)
    #     if r:
    #         return r  # retourne une string
    #     return None

    def getRasp(self, idRasp):
        return self.rdao.findById(idRasp)
    
    def supprimeR(self, idLecteur):
        return self.rdao.deleteRasp(idLecteur)
    
    def verifieShellRasp(self):
        return self.rdao.verifieShell()
    
    def envoieChaqueChangementPlanning(self):
        time.sleep(10)  # Attendre 10 secondes le temps que les fichiers json se mettent à jour
        raspberrys = self.rdao.findAll()
        for r in raspberrys:
            if r["ip"] is None or r["nomLecteur"] is None:
                continue  # Ignorer les entrées avec des informations incomplètes
            subprocess.run(["rsync", "-avz", "--delete", "-e", "ssh","./app/static/rasdata/",  f"{r['nomLecteur']}@{r['ip']}:/home/{r['nom']}/musiquali/"])
            time.sleep(5)
            subprocess.run(["ssh", f"{r['nom']}@{r['ipRasp']}", "python3", f"/home/{r['nom']}/musiquali/RAS.py"])

    # def pingTout(self): #pour les logs
    #     toutRasp = self.montreToutRasp()
    #     for chaque in toutRasp:
    #             subprocess.run(["ping", "-c", "1", chaque["ipRasp"]])

    def triASC(self):
        return self.rdao.triASC()
    
    def triDESC(self):
        return self.rdao.triDESC()
    
    def triIP(self):
        return self.rdao.triIP()
    
    def recherche(self, query):
        return self.rdao.recherche(query)

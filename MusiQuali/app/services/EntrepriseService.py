from app.DAO.EntrepriseDAO import EntrepriseSqliteDAO as EntrepriseDAO
import subprocess, ipaddress, time
from flask import render_template, request, redirect, url_for, flash

class EntrepriseService:

    def __init__(self):
        self.edao = EntrepriseDAO()

    def createEntreprise(self, nomEntreprise):
        # Validation métier
        if not nomEntreprise or len(nomEntreprise.strip()) == 0:
            raise ValueError("Le nom de l'entreprise est obligatoire")

        # Vérifier l'unicité
        entreprise = self.edao.findByName(nomEntreprise)
        if entreprise:
            raise ValueError("Cette entreprise existe déjà")

        return self.edao.createEntreprise(nomEntreprise)

    def getAllEntreprises(self):
        return self.edao.findAll()

    def getEntrepriseById(self, idEntreprise):
        entreprise = self.edao.findById(idEntreprise)

        if not entreprise:
            raise ValueError("Entreprise introuvable")

        return entreprise

    def getEntrepriseByName(self, nomEntreprise):
        return self.edao.findByName(nomEntreprise)
    
    def getEntrepriseIdByName(self, idEntreprise):
        return self.edao.findIdbyName(idEntreprise)

    def deleteEntreprise(self, idEntreprise):
        entreprise = self.edao.findById(idEntreprise)

        if not entreprise:
            raise ValueError("Entreprise introuvable")

        return self.edao.delete(idEntreprise)

        
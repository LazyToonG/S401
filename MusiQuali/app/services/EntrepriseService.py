from app.DAO.EntrepriseDAO import EntrepriseSqliteDAO as EntrepriseDAO
import subprocess, ipaddress, time
from flask import render_template, request, redirect, url_for, flash

class EntrepriseService:

    def __init__(self):
        self.edao = EntrepriseDAO()

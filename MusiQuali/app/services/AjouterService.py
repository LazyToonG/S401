from app.DAO.AjouterDAO import AjouterSqliteDAO as AjouterDAO
import subprocess, ipaddress, time
from flask import render_template, request, redirect, url_for, flash

class AjouterService:

    def __init__(self):
        self.edao = AjouterDAO()

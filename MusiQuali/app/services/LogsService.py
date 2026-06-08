from app.DAO.LogsDAO import LogsSqliteDAO as LogsDAO
import subprocess, ipaddress, time
from flask import render_template, request, redirect, url_for, flash

class LogsService:

    def __init__(self):
        self.edao = LogsDAO()

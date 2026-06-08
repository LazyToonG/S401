from app.DAO.MessageDAO import MessageSqliteDAO as MessageDAO
import subprocess, ipaddress, time
from flask import render_template, request, redirect, url_for, flash

class MessageService:

    def __init__(self):
        self.edao = MessageDAO()

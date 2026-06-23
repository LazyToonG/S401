from app.DAO.LogsDAO import LogsSqliteDAO as LogsDAO
import subprocess, ipaddress, time, os
from flask import render_template, request, redirect, url_for, flash
from pathlib import Path


class LogsService:

    def __init__(self):
        self.edao = LogsDAO()

    # ---------------- DB ----------------

    def get_all_logs(self):
        return self.edao.get_all()

    def get_logs_by_raspberry(self, id_rasp):
        return self.edao.get_by_raspberry(id_rasp)

    def add_log(self, id_rasp, filename):
        return self.edao.insert(id_rasp, filename)

    def get_latest_log(self):
        return self.edao.get_latest()

    def delete_log(self, id):
        return self.edao.delete(id)

    # ---------------- FILE SYSTEM ----------------

    def list_log_files(self, nom_lecteur):
        base = Path(__file__).resolve().parent.parent / "static" / "raspLogs"
        path = (base / nom_lecteur / "logs").resolve()

        if base not in path.parents and path != base:
            return []
        if not path.exists():
            return []

        return sorted([f.name for f in path.iterdir() if f.is_file()])

    def read_log_file(self, nom_lecteur, filename):
        base = Path(__file__).resolve().parent.parent / "static" / "raspLogs"
        path = (base / nom_lecteur / "logs" / filename).resolve()

        if base not in path.parents:
            return None
        if not path.exists() or not path.is_file():
            return None

        return path.read_text(encoding="utf-8", errors="ignore")
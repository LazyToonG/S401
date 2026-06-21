from app.models.Planning import Planning
from app.DAO.PlanningDAO import PlanningDAO
from app import app
import os
import json
import shutil


DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


class PlanningService:
    """
    Couche service pour le planning (calendrier des commerciaux/playlists
    et calendrier des messages).

    Le front envoie l'état complet du calendrier au moment du Save :
    une liste de "boxes", chacune avec soit idPlaylist soit idMSG (jamais les
    deux), un StartTime (ISO 8601), et optionnellement idPlanning si la box
    existe déjà en bd (auquel cas c'est un update, sinon une création).

    Le service calcule le diff par rapport à ce qui est en bd : les lignes
    absentes du payload sont supprimées, les nouvelles sont insérées, celles
    avec idPlanning connu sont mises à jour.
    """

    def __init__(self):
        self.dao = PlanningDAO()
        self.export_dir = os.path.join(app.static_folder, "rasData")
        self.sound_dir = os.path.join(self.export_dir, "rasSound")
        self.source_music_dir = os.path.join(app.static_folder, "AllMusics")

    def get_all(self, idEntreprise=1):
        """Retourne tout le planning pour une entreprise (état initial des calendriers)."""
        return self.dao.get_all(idEntreprise)

    def sync(self, boxes, idEntreprise=1):
        """
        boxes: liste de dicts, chacun avec les clés possibles:
            - idPlanning (int ou None) : None si la box n'existe pas encore en bd
            - idPlaylist (int ou None)
            - idMSG (int ou None)
            - StartTime (str ISO 8601)

        Retourne la liste des Planning à jour (avec idPlanning rempli pour les
        nouvelles entrées), pour que le front puisse re-synchroniser ses boxes.
        """
        existing = self.dao.get_all(idEntreprise)
        existing_ids = {p.idPlanning for p in existing}
        incoming_ids = set()

        results = []

        for box in boxes:
            idPlaylist = box.get("idPlaylist")
            idMSG = box.get("idMSG")

            if (idPlaylist is None) == (idMSG is None):
                # garde-fou : une box doit avoir exactement l'un des deux
                raise ValueError(
                    "Chaque box doit référencer soit idPlaylist soit idMSG (jamais les deux, ni aucun)."
                )

            start_time = box.get("StartTime")
            if not start_time:
                raise ValueError("StartTime est requis pour chaque box.")

            planning = Planning(
                idPlanning=box.get("idPlanning"),
                idPlaylist=idPlaylist,
                idMSG=idMSG,
                StartTime=start_time,
                idEntreprise=idEntreprise
            )

            saved = self.dao.create(planning)  # create() gère insert ou update
            incoming_ids.add(saved.idPlanning)
            results.append(saved)

        # Supprime en bd ce qui n'est plus présent côté calendrier
        removed_ids = existing_ids - incoming_ids
        for planning_id in removed_ids:
            self.dao.delete(planning_id)

        return results

    def delete(self, planning_id):
        """Supprime une entrée précise du planning."""
        self.dao.delete(planning_id)

    # -------------------- Export (MU.json / MSG.json / rasSound) --------------------

    @staticmethod
    def _day_name_from_start_time(start_time):
        """Extrait le nom de jour (monday..sunday) d'un StartTime ISO 8601."""
        from datetime import datetime
        dt = datetime.fromisoformat(start_time)
        return DAY_NAMES[dt.weekday()]  # 0 = monday ... 6 = sunday

    @staticmethod
    def _time_str_from_start_time(start_time):
        """Extrait l'heure HH:MM d'un StartTime ISO 8601."""
        from datetime import datetime
        dt = datetime.fromisoformat(start_time)
        return dt.strftime("%H:%M")

    def _build_day_skeleton(self):
        return {day: [] for day in DAY_NAMES}

    def export_planning(self, idEntreprise=1):
        """
        Génère MU.json (playlists), MSG.json (messages), et copie les mp3
        référencés dans static/rasData/rasSound. Tout est régénéré à neuf
        à chaque appel (le dossier rasSound est vidé puis reconstruit).

        Format de chaque fichier :
        {
            "monday": [ {"time": "13:30", "musics": ["a.mp3", "b.mp3"]}, ... ],
            "tuesday": [...],
            ...
        }
        Les jours sans créneau ont une liste vide.
        """
        message_slots = self.dao.get_message_slots(idEntreprise)
        playlist_slots = self.dao.get_playlist_slots(idEntreprise)

        msg_data = self._build_day_skeleton()
        mu_data = self._build_day_skeleton()
        needed_filenames = set()

        for slot in message_slots:
            day = self._day_name_from_start_time(slot["StartTime"])
            time_str = self._time_str_from_start_time(slot["StartTime"])
            filename = slot["nomMusique"]

            msg_data[day].append({"time": time_str, "musics": [filename]})
            needed_filenames.add(filename)

        for slot in playlist_slots:
            day = self._day_name_from_start_time(slot["StartTime"])
            time_str = self._time_str_from_start_time(slot["StartTime"])
            filenames = slot["musics"]  # déjà triés par position

            mu_data[day].append({"time": time_str, "musics": filenames})
            needed_filenames.update(filenames)

        # Trie chaque jour par heure, pour un fichier lisible/déterministe
        for day in DAY_NAMES:
            msg_data[day].sort(key=lambda s: s["time"])
            mu_data[day].sort(key=lambda s: s["time"])

        os.makedirs(self.export_dir, exist_ok=True)

        with open(os.path.join(self.export_dir, "MSG.json"), "w", encoding="utf-8") as f:
            json.dump(msg_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(self.export_dir, "MU.json"), "w", encoding="utf-8") as f:
            json.dump(mu_data, f, ensure_ascii=False, indent=2)

        self._refresh_sound_folder(needed_filenames)

        return {"msg": msg_data, "mu": mu_data, "copied_files": sorted(needed_filenames)}

    def _refresh_sound_folder(self, needed_filenames):
        """Vide rasSound puis copie uniquement les mp3 actuellement planifiés."""
        if os.path.isdir(self.sound_dir):
            shutil.rmtree(self.sound_dir)
        os.makedirs(self.sound_dir, exist_ok=True)

        missing = []
        for filename in needed_filenames:
            source_path = os.path.join(self.source_music_dir, filename)
            if os.path.exists(source_path):
                shutil.copy2(source_path, os.path.join(self.sound_dir, filename))
            else:
                missing.append(filename)

        if missing:
            # Ne bloque pas l'export, mais on garde une trace des fichiers introuvables
            print(f"[PlanningService] Fichiers mp3 introuvables, non copiés: {missing}")
from app.DAO.ScheduleDAO import ScheduleDAO
from app.models.Scheduler import Schedule
from app.models.Music import Music
import io
import json

class ScheduleService:
    def __init__(self):
        self.schedule_dao = ScheduleDAO()
        self.schedule_dao.init_db()

    def _load_planning(self):
        planning_data = {"start_time": "00:00"}
        # Utiliser les jours en minuscules comme dans la BD
        days_lowercase = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        days_capitalized = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day_lower, day_cap in zip(days_lowercase, days_capitalized):
            start_time = self.schedule_dao.get_start_time(day_lower)
            items = self.schedule_dao.get_items_by_day(day_lower)
            musics = []
            for item in items:
                m = Music(item['id'], item['title'], item['path'], item['duration'])
                m.artist = item['artist']
                musics.append(m)
            # Utiliser la version capitalisée pour le modèle
            planning_data[day_cap] = [start_time] + musics
        return Schedule(planning_data)

    def get_planning(self):
        # Recharger les données depuis la BD à chaque appel pour avoir les données fraîches
        return self._load_planning()

    def sync_day(self, day, tasks, start_time):
        # Normaliser le jour en minuscules (le JavaScript l'envoie en minuscules)
        day = day.lower()
        
        # Mise à jour de la Base de Données via DAO
        self.schedule_dao.update_start_time(day, start_time)
        self.schedule_dao.clear_day_items(day)
        for i, t in enumerate(tasks):
            try:
                duration = int(t.get('duration', 0))
            except (ValueError, TypeError):
                duration = 0
            self.schedule_dao.add_item(day, i, t.get('title', 'Sans titre'), t.get('artist', ''), duration, t.get('path', ''))

    def move_task(self, from_day, from_index, to_day, to_index):
        # Cette méthode est utilisée par le contrôleur mais le drag-drop est géré côté client
        # Pour l'instant, on ne fait rien car la synchronisation se fait via sync_day
        pass

    def export_planning(self):
        days_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        planning = self._load_planning()  # Recharger les données fraîches
        export_data = {}
        
        for day in days_order:
            day_data = getattr(planning, day)
            if not day_data:
                continue
            
            start_time = day_data[0]
            music_names = [m.titre for m in day_data[1:]]
            
            # Format: { "day": [["HH:MM"], "song1", "song2", ...] }
            export_data[day] = [[start_time]] + music_names
        
        # Convertir en JSON et créer un fichier en mémoire
        json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
        mem_file = io.BytesIO(json_str.encode('utf-8'))
        mem_file.seek(0)
        return mem_file

service_schedule = ScheduleService()
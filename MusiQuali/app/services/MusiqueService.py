import os
from app.DAO.MusicDAO import MusicDAO
from mutagen.mp3 import MP3
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #2x pour pointer vers app plutot que service

# Set upload folder relative to the app structure
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "rasdata", "allMusic")
ALLOWED_EXTENSIONS = {"mp3"}

# Make sure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class MusiqueService:
    def __init__(self):
        self.dao = MusicDAO()
        self.upload_folder = UPLOAD_FOLDER
    
    def get_musiques(self, sort="title"):
        return self.dao.get_musiques(order_by=sort)

    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_file(self, file):
        if file.filename == "":
            raise ValueError("Aucun fichier sélectionné")
        if not self.allowed_file(file.filename):
            raise ValueError("Format non autorisé")

        filename = secure_filename(file.filename)
        title = os.path.splitext(filename)[0]
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)

        audio = MP3(filepath) #mutagen pour gerer les mp3
        duration = int(audio.info.length)

        # DAO retourne un objet Music
        return self.dao.create(title=title, path=filepath, duration=duration)

    def delete_musique(self, music):
        self.dao.delete(music.id)
        if os.path.exists(music.path):  
            os.remove(music.path)
    def get_by_id(self, music_id):
        a=MusicDAO()
        return a.get_by_id(music_id)
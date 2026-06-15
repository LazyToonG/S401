from app.DAO.PlaylistDAO import PlaylisteDAO
from app.DAO.MusicDAO import MusicDAO
import os
from mutagen.mp3 import MP3
from werkzeug.utils import secure_filename
from app import app

class MarketingService:

    def __init__(self):
        self.playlistDAO = PlaylisteDAO()
        self.musicDAO = MusicDAO()

    def get_playlists(self):
        return self.playlistDAO.get_all()

    def get_all_musics(self):
        return self.musicDAO.get_musiques()

    def get_playlist_tracks(self, playlist_id):
        """Retourne la liste des musiques associées à une playlist."""
        playlist = self.playlistDAO.get(playlist_id)
        if not playlist:
            return []

        ids = self.playlistDAO._str_to_ids(getattr(playlist, "musiques", None))
        all_musics = {m.idMusique: m for m in self.musicDAO.get_all()}

        return [all_musics[i] for i in ids if i in all_musics]

    def get_marketing_data(self):
        return {
            "playlists": self.get_playlists(),
            "musiques": self.get_all_musics(),
            "musics": self.get_all_musics(),
        }

    def add_music(self, nomMusique, duree, idEntreprise=1):
        return self.musicDAO.create(nomMusique, duree, idEntreprise)

    def delete_music(self, idMusique):
        self.musicDAO.delete(idMusique)

    def delete_playlist(self, idPlaylist):
        self.playlistDAO.delete(idPlaylist)

    



    def save_music_file(self, file):
        
        #Sauvegarde le fichier mp3 dans app/static/AllMusics
        #et enregistre la musique en base de données.
        #Retourne l'objet Music créé pour la bd
        
        filename = secure_filename(file.filename) #!!! securefilename modifie les accents/charactères spéciaux
        nomMusique = filename  # nomMusique = "AllMusics/{nom.mp3}" 

        folder = os.path.join(app.static_folder, "AllMusics")
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, filename)
        file.save(filepath)

        # Extraction de la durée (en secondes, arrondie)
        try:
            audio = MP3(filepath)
            duree = int(audio.info.length)
        except Exception:
            duree = 0

        return self.musicDAO.create(nomMusique, duree)

    def save_music_files(self, files):
        """Sauvegarde plusieurs fichiers mp3, retourne la liste des Music créées."""
        created = []
        for file in files:
            if file and file.filename:
                created.append(self.save_music_file(file))
        return created